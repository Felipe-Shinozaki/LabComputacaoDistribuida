from mpi4py import MPI
import random
import time

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

N = 300 # Altere para 600 e 1000 para os próximos testes

if rank == 0:
    A = [[random.random() for _ in range(N)] for _ in range(N)]
    B = [[random.random() for _ in range(N)] for _ in range(N)]
    inicio = time.time()
else:
    A = None
    B = None

# Distribui as matrizes para todos os processos
A = comm.bcast(A, root=0)
B = comm.bcast(B, root=0)

# Calcula a fatia de linhas para cada processo
linhas_por_proc = N // size
inicio_linha = rank * linhas_por_proc
fim_linha = N if rank == size - 1 else (rank + 1) * linhas_por_proc

# Cálculo local
C_local = []
for i in range(inicio_linha, fim_linha):
    linha = [0] * N
    for j in range(N):
        for k in range(N):
            linha[j] += A[i][k] * B[k][j]
    C_local.append(linha)

# Reúne os resultados no processo 0
C_gather = comm.gather(C_local, root=0)

if rank == 0:
    C_final = [linha for sublist in C_gather for linha in sublist]
    fim = time.time()
    print(f"Tempo Distribuído MPI (N={N}): {(fim - inicio) * 1000:.2f} ms")