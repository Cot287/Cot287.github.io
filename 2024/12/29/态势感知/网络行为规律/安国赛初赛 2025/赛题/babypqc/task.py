import ctypes
from random import getrandbits
import signal
import socketserver
from sympy import nextprime
import numpy as np  
from Crypto.Util.number import *
import ast


def ll_to_polylist(l):
    return list(map(list, list(l)))

class Dilithium:
    def __init__(self):
        self.dilithium_lib = ctypes.CDLL("./dilithium/libpqcrystals_dilithium2_ref.so")
        self.pk_buf = ctypes.c_buffer(1312)
        self.sk_buf = ctypes.c_buffer(2560)
        self.Q = 8380417
        self.N = 256
        self.dilithium_lib.pqcrystals_dilithium2_ref_keypair(self.pk_buf, self.sk_buf)

    def sign_message(self, message: bytes) -> bytes:
        SIGNLEN = 2420
        MLEN = len(message)
        sm_buf = ctypes.create_string_buffer(SIGNLEN + MLEN)
        m_buf = ctypes.create_string_buffer(message)
        smlen_buf = ctypes.c_size_t()
        self.dilithium_lib.pqcrystals_dilithium2_ref(sm_buf, ctypes.byref(smlen_buf), m_buf, MLEN, self.sk_buf)
        return sm_buf.raw[:smlen_buf.value]

    def verify_sign(self, message: bytes, signature: bytes) -> bool:
        msg_buf = ctypes.create_string_buffer(len(signature))
        msg_len = ctypes.c_size_t()
        sm_buf = ctypes.create_string_buffer(signature)
        result = self.dilithium_lib.pqcrystals_dilithium2_ref_open(msg_buf, ctypes.byref(msg_len), sm_buf, len(signature), self.pk_buf)
        return result == 0 and message == msg_buf.raw[:msg_len.value]

class Task(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def timeout_handler(self, signum, frame):
        raise TimeoutError

    def dosend(self, msg):
        try:
            self.request.sendall(msg.encode('latin-1') + b'\n')
        except:
            pass

    def recvline(self, msg = None):
        if msg:
            self.request.sendall(msg.encode('latin-1'))
        try:
            data = b""
            while True:
                chunk = self.request.recv(1)
                if not chunk:
                    break
                data += chunk
                if chunk == b'\n':
                    break
        except:
            pass

        line = data.strip().decode()
        return line
        
    def generate_prime(self, BITS):
        a = getrandbits(BITS)
        b = a << 282
        c = nextprime(b)
        return c

    def generate_coefs(self, BITS, LEN):
        return [getrandbits(BITS) for _ in range(LEN)]

    def get_sk(self):
        poly_t = ctypes.c_int32 * self.dilithium.N
        polyvec_t = poly_t * 4
        rho = ctypes.c_buffer(32)
        tr = ctypes.c_buffer(64)
        key = ctypes.c_buffer(32)
        t0 = polyvec_t()
        s1 = polyvec_t()
        s2 = polyvec_t()
        self.dilithium.dilithium_lib.pqcrystals_dilithium2_ref_unpack_sk(rho, tr, key, t0, s1, s2, self.dilithium.sk_buf)
        return ll_to_polylist(s1), ll_to_polylist(s2)

    def handle(self):
        signal.signal(signal.SIGALRM, self.timeout_handler)
        signal.alarm(40)
        self.dosend("welcome to my crypto system!")
        delta = 1184
        beta = 256
        tau = 704
        self.m = getrandbits(beta)
        self.dilithium = Dilithium()

        p = self.generate_prime(delta)
        q = self.generate_prime(delta)
        N = [p * q]
        ROUND = 25
        for _ in range(ROUND):
            d = getrandbits(704)
            N.append((p + d) * (q + d))
        self.dosend("N = " + str(N))
        s1, s2 = self.get_sk()
        s1 = np.array([i for j in s1 for i in j])
        s2 = np.array([i for j in s2 for i in j])
        H = []
        for i in range(ROUND * ROUND):
            tmp = np.array(self.generate_coefs(32, 1024))
            H.append(int(tmp.dot(s1) % self.dilithium.Q ))
            tmp = np.array(self.generate_coefs(32, 1024))
            H.append(int(tmp.dot(s2) % self.dilithium.Q))

        self.dosend("this is your hint!")
        self.dosend("H = " + str(H))
        self.dosend("another gift: you can choose one message to sign")
        m = int(self.recvline("m: "))
        signature = self.dilithium.sign_message(long_to_bytes(m))
        assert self.dilithium.verify_sign(long_to_bytes(m), signature)
        self.dosend("this is your signature")
        self.dosend("sinature = " + signature.hex())
        num = self.generate_coefs(4, 1)[0]
        self.dosend("you need to give me some signatures in hex format!")
        signatures = ast.literal_eval(self.recvline("signatures: "))
        assert len(list(set(signatures))) == len(signatures)
        answers = sum([self.dilithium.verify_sign(long_to_bytes(self.m), bytes.fromhex(sinature.zfill(len(signature) + len(signature)%2))) for sinature in signatures])
        if answers == num:
            self.dosend("congrats! you got the flag!")
            with open("flag.txt") as f:
                self.dosend(f.read())
        else:
            self.dosend("sorry, you failed!")
            exit()

class ThreadedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 13337
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()


