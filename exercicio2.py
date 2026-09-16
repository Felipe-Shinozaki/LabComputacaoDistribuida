from mpi4py import MPI
import random
import time

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

N_total = 10_000_000
N_local = N_total // size

if rank == 0:
    inicio = time.time()

dentro_local = 0
for _ in range(N_local):
    x = random.random()
    y = random.random()
    if x*x + y*y <= 1.0:
        dentro_local += 1

# Soma os resultados locais no rank 0 usando MPI.SUM
dentro_total = comm.reduce(dentro_local, op=MPI.SUM, root=0)

if rank == 0:
    pi_estimado = 4.0 * (dentro_total / N_total)
    fim = time.time()
    print(f"PI aproximado: {pi_estimado:.6f}")
    print(f"Tempo Distribuído MPI: {(fim - inicio) * 1000:.2f} ms")