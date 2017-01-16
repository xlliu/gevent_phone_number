from multiprocessing import Pool
def f(x):
  return 1/0
  
if __name__ == '__main__':
  pool = Pool(processes=1)
  # Start a worker processes.
  result = pool.apply_async(f, [10]) 