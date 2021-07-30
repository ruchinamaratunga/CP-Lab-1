import os
import shutil
import pandas as pd
import sys
import matplotlib.pyplot as plt
import statistics

cwd = os.getcwd()

if os.path.exists(str(cwd) + "/diagrams"):
    shutil.rmtree(str(cwd) + "/diagrams")
else:
    pass

if os.path.exists(str(cwd) + "/results"):
    shutil.rmtree(str(cwd) + "/results")
else:
    pass

try:
  os.mkdir(str(cwd) + "/diagrams")
except:
  pass

try:
  os.mkdir(str(cwd) + "/diagrams/comparison")
except:
  pass

try:
  os.mkdir(str(cwd) + "/diagrams/individual")
except:
  pass

try:
  os.mkdir(str(cwd) + "/results")
except:
  pass

try:
  os.mkdir(str(cwd) + "/results/total_results")
except:
  pass

try:
  os.mkdir(str(cwd) + "/results/total_n")
except:
  pass

# c_file = sys.argv[1]
# thread_count = int(sys.argv[2])
# n = int(sys.argv[3])
# m = int(sys.argv[4])
# m_fraction = float(sys.argv[5])
# i_fraction = float(sys.argv[6])
# d_fraction = float(sys.argv[7])
# number_of_iterations = int(sys.argv[8])

# c_file = sys.argv[1]
# n = int(sys.argv[2])
# m = int(sys.argv[3])
# m_fraction = float(sys.argv[4])
# i_fraction = float(sys.argv[5])
# d_fraction = float(sys.argv[6])
# number_of_iterations = int(sys.argv[7])

thread_count_column = 'number of threads'
n_column = 'n'
m_column = 'm'
member_fraction_column = 'fraction of member operations'
insert_fraction_column = 'fraction of insert operations'
delete_fraction_column = 'fraction of delete operations'
iteration_column= 'number of iterations'
node_count = 'remaining nodes'
time_column = "Execution Time"
median_column = "median"
std_column = "Std"
iters = "Iterations"

method_name_column = "Method"

thread_1_avg_column = "Average time for 1 thread"
thread_2_avg_column = "Average time for 2 thread"
thread_3_avg_column = "Average time for 4 thread"
thread_4_avg_column = "Average time for 8 thread"

thread_1_std_column = "Std time for 1 thread"
thread_2_std_column = "Std time for 2 thread"
thread_3_std_column = "Std time for 4 thread"
thread_4_std_column = "Std time for 8 thread"

# times_df = pd.DataFrame(columns=[thread_1_avg_column, thread_1_std_column, thread_2_avg_column, thread_2_std_column, thread_3_avg_column, thread_3_std_column, thread_4_avg_column, thread_4_std_column])
c_files = {"Serial": "sequential_test", "mutex": "mutex_test", "read write lock": "read_write_lock"}

def plot_thread_and_avgtime_graph(x, y, index, method_name, title):
  if (index % 3 == 0):
    color = 'r'
  elif (index % 3 == 1):
    color = 'b' 
  else:
    color = 'g'
  # title = '170024R , 170031K' + title +")"
  plt.plot(x, y, color= color, label = method_name)
  plt.xlabel('Thread count')
  plt.ylabel('Average time(s)')
  plt.title("170024R, 170031K Execution time for " + title)
  # plt.show()

def plot_thread_and_avgtime_for_method_graph(method_name):
  file1 = cwd + "/results/Average and Std 10000 1000 0.5 0.25 0.25.csv"
  file2 = cwd + "/results/Average and Std 10000 1000 0.9 0.05 0.05.csv"
  file3 = cwd + "/results/Average and Std 10000 1000 0.99 0.005 0.005.csv"
  color1 = 'r'
  color2 = 'b' 
  color3 = 'g'

  df1 = pd.read_csv(file1)
  df2 = pd.read_csv(file2)
  df3 = pd.read_csv(file3)

  df1 = df1[[thread_1_avg_column, thread_2_avg_column, thread_3_avg_column, thread_4_avg_column]].loc[df1[method_name_column] == method_name]
  df2 = df2[[thread_1_avg_column, thread_2_avg_column, thread_3_avg_column, thread_4_avg_column]].loc[df2[method_name_column] == method_name]
  df3 = df3[[thread_1_avg_column, thread_2_avg_column, thread_3_avg_column, thread_4_avg_column]].loc[df3[method_name_column] == method_name]

  cases = ["10000 1000 0.5 0.25 0.25", "10000 1000 0.9 0.05 0.05", "10000 1000 0.99 0.005 0.005"]
  time_list = [df1.values, df2.values, df3.values]
  x = ['1', '2', '4', '8']
  i = -1
  plt.clf()
  for case in time_list:
    i +=1
    if ( i% 3 == 0):
      color = color1
    elif(i%2 == 0):
      color = color2
    else:
      color = color3
    # print(case)
    plt.plot(x, case.flatten(), color= color, label = cases[i])
    plt.xlabel('Thread count')
    plt.ylabel('Average time(s)')
    plt.title("170024R, 170031K Execution time for " + method_name + " for each cases")
  plt.legend()
  plt.show()
  plt.savefig("diagrams/individual/" + str(method_name) + ".png")
  plt.clf()

def execute(c_file, n, m, m_fraction, i_fraction, d_fraction, number_of_iterations):
  df = pd.DataFrame(columns=[thread_count_column, n_column, m_column, member_fraction_column, insert_fraction_column, delete_fraction_column, iteration_column, node_count, time_column])
  thread_counts = [1,2,4,8]
  dataframe_row = 0
  for thread_count in thread_counts:
      for j in range(int(number_of_iterations)):
          os.system("./" + str(c_file) + ".out " + str(thread_count) + " " + str(n) + " " + str(m) + " " + str(m_fraction) + " " + str(i_fraction) + " " + str(d_fraction) + " > " + str(c_file) + ".txt")
          with open(str(c_file) + ".txt", "r") as f:
              outputs = f.read().splitlines()
              count = int(outputs[1].split(":")[1].strip())
              time = float(outputs[2].split(":")[1].strip())
              df.loc[dataframe_row + j] = [int(thread_count), int(n), int(m), m_fraction, i_fraction, d_fraction, int(number_of_iterations), int(count), time]
      dataframe_row += number_of_iterations
  df.to_csv("results/total_results/results " + str(c_file) + " - " + str(n) + " " + str(m) + " " + str(m_fraction) + " " + str(i_fraction) + " " + str(d_fraction) + ".csv")
  return df

def get_iterations(c_file, n, m, m_fraction, i_fraction, d_fraction, number_of_iterations = 10):
  df_n = pd.DataFrame(columns=[thread_count_column, n_column, m_column, member_fraction_column, insert_fraction_column, delete_fraction_column, iteration_column, node_count, median_column, std_column, iters])
  thread_counts = [1,2,4,8]
  dataframe_row = 0
  for thread_count in thread_counts:
    sum_count = 0
    times_count = []
    std= 0
    for j in range(int(number_of_iterations)):
      os.system("./" + str(c_file) + ".out " + str(thread_count) + " " + str(n) + " " + str(m) + " " + str(m_fraction) + " " + str(i_fraction) + " " + str(d_fraction) + " > " + str(c_file) + ".txt")
      with open(str(c_file) + ".txt", "r") as f:
          outputs = f.read().splitlines()
          count = int(outputs[1].split(":")[1].strip())
          time = float(outputs[2].split(":")[1].strip())
          sum_count += time
          times_count.append(time)
    std = statistics.stdev(times_count)
    median = sum_count / number_of_iterations
    number = (100 * 1.96 * std / ( median* 5)) ** 2
    df_n.loc[dataframe_row] = [int(thread_count), int(n), int(m), m_fraction, i_fraction, d_fraction, int(number_of_iterations), int(count), median, std, number]
    dataframe_row += 1
  df_n.to_csv("results/total_n/results " + str(c_file) + " " + str(n) + " " + str(m) + " " + str(m_fraction) + " " + str(i_fraction) + " " + str(d_fraction) + ".csv")
  return df_n

def avg_and_std(df, method_name, index, output_df, n, m, m_fraction, i_fraction, d_fraction):  
  thread_1_df = df.loc[df[thread_count_column] == 1]
  thread_2_df = df.loc[df[thread_count_column] == 2]
  thread_4_df = df.loc[df[thread_count_column] == 4]
  thread_8_df = df.loc[df[thread_count_column] == 8]

  thread_1_mean_value = thread_1_df[time_column].mean()
  thread_2_mean_value = thread_2_df[time_column].mean()
  thread_4_mean_value = thread_4_df[time_column].mean()
  thread_8_mean_value = thread_8_df[time_column].mean()

  thread_1_std_value = thread_1_df[time_column].std()
  thread_2_std_value = thread_2_df[time_column].std()
  thread_4_std_value = thread_4_df[time_column].std()
  thread_8_std_value = thread_8_df[time_column].std()

  x = ['1', '2', '4', '8']
  y = [thread_1_mean_value, thread_2_mean_value, thread_4_mean_value, thread_8_mean_value]

  plot_thread_and_avgtime_graph(x, y, index,method_name, str(n) + " " + str(m) + " " + str(m_fraction) + " " + str(i_fraction) + " " + str(d_fraction))

  output_df.loc[index] = [method_name, thread_1_mean_value, thread_1_std_value, thread_2_mean_value, thread_2_std_value, thread_4_mean_value, thread_4_std_value, thread_8_mean_value, thread_8_std_value]

  return output_df

# plot the average execution time against num of threads

def process(n, m, m_fraction, i_fraction, d_fraction, number_of_iterations):
  index = 0
  times_df = pd.DataFrame(columns=[method_name_column, thread_1_avg_column, thread_1_std_column, thread_2_avg_column, thread_2_std_column, thread_3_avg_column, thread_3_std_column, thread_4_avg_column, thread_4_std_column])
  for method in c_files:
    df = pd.DataFrame(columns=[thread_count_column, n_column, m_column, member_fraction_column, insert_fraction_column, delete_fraction_column, iteration_column, node_count, time_column])
    get_iterations(c_files[method], n, m, m_fraction, i_fraction, d_fraction, number_of_iterations)
    result1 = execute(c_files[method], n, m, m_fraction, i_fraction, d_fraction, number_of_iterations)
    result2 = avg_and_std(result1, method, index + 1, times_df, n, m, m_fraction, i_fraction, d_fraction)
    index += 1
  times_df.to_csv("results/Average and Std " + str(n) + " " + str(m) + " " + str(m_fraction) + " " + str(i_fraction) + " " + str(d_fraction) + ".csv")
  plt.legend()
  plt.show()
  plt.savefig("diagrams/comparison/Average and Std " + str(n) + " " + str(m) + " " + str(m_fraction) + " " + str(i_fraction) + " " + str(d_fraction) + '.png')
  plt.clf()

process(1000, 10000, .99, .005, .005, 30)
process(1000, 10000, .9, .05, .05, 30)
process(1000, 10000, .5, .25, .25, 30)

for key in c_files:
  plot_thread_and_avgtime_for_method_graph(str(key))