#!/usr/bin/python3

# The scripts sums all coverage results of the built packages in a catkin tools workspace and outputs it to the terminal.
# First build all packages in the workspace with coverage enabled using: catkin build --verbose --catkin-make-args run_coverage -- --force-cmake -DCMAKE_BUILD_TYPE=Debug
# Then run this script with: python3 sum_coverage.py PATH_TO_CATKIN_WS

import subprocess
import os
import sys

def getNumberOfCoveredLines(file):
  return getLineCoverageValue(file, 1);

def getNumberOfLines(file):
  return getLineCoverageValue(file, 2);

def getCoverageValue(file, n):
  ps = subprocess.Popen(('grep', '-oP', "(?<=<td class=\"headerCovTableEntry\">).*?(?=</td>)", file), stdout=subprocess.PIPE)
  output = int(subprocess.check_output(('sed', '{}q;d'.format(n)), stdin=ps.stdout).decode("utf-8"))
  ps.wait()
  return output

def getCoverage(catkin_dir, count_id, covered_count_id):
    count = 0
    covered_count = 0
    catkin_build_dir = os.path.join(catkin_dir, 'build')
    packages = os.listdir(catkin_build_dir)
    for root, dirs, files in os.walk(catkin_build_dir):
        for file in files:
            for package in packages:
                if os.path.join(root, file).endswith("cmake_code_coverage/" + package + "/index.html"):
                    file_path = os.path.join(root, file);
                    count += getCoverageValue(file_path, count_id)
                    covered_count += getCoverageValue(file_path, covered_count_id)
    return (count, covered_count)

def getLineCoverage(catkin_dir):
    return getCoverage(catkin_dir, 2, 1)

def getFunctionCoverage(catkin_dir):
    return getCoverage(catkin_dir, 4, 3)

def main():
  if len(sys.argv) > 1:
    catkin_dir = sys.argv[1]
  else:
    catkin_dir = os.getcwd()

  nr_lines, nr_covered_lines = getLineCoverage(catkin_dir)
  print("Number of Lines: {}".format(nr_lines))
  print("Number of Lines Covered: {}".format(nr_covered_lines))
  print("Line Coverage: {}%".format(round(nr_covered_lines/nr_lines*100.0,2)))
  nr_functions, nr_covered_functions = getFunctionCoverage(catkin_dir)
  print("Number of Functions: {}".format(nr_functions))
  print("Number of Functions Covered: {}".format(nr_covered_functions))
  print("Functions Coverage: {}%".format(round(nr_covered_functions/nr_functions*100.0,2)))


if __name__ == "__main__":
  main()
