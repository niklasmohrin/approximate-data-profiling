# Hyperfine (includes jvm startup)
```shell
$ hyperfine --warmup 3 --runs 10 --parameter-list input 'adult_kmeans_0.001.csv,adult_kmeans_0.01.csv,adult_kmeans_0.1.csv,adult_random_0.001.csv,adult_random_0.01.csv,adult_random_0.1.csv,adult.csv' 'java -Dtinylog.level=trace -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files ../data/{input} --file-key INPUT_GENERATOR'
Benchmark 1: java -Dtinylog.level=trace -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files ../data/adult_kmeans_0.001.csv --file-key INPUT_GENERATOR
  Time (mean ± σ):     695.0 ms ±  19.8 ms    [User: 1800.7 ms, System: 79.2 ms]
  Range (min … max):   651.6 ms … 723.7 ms    10 runs

Benchmark 2: java -Dtinylog.level=trace -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files ../data/adult_kmeans_0.01.csv --file-key INPUT_GENERATOR
  Time (mean ± σ):     653.1 ms ±  27.1 ms    [User: 1722.5 ms, System: 90.0 ms]
  Range (min … max):   618.0 ms … 695.6 ms    10 runs

Benchmark 3: java -Dtinylog.level=trace -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files ../data/adult_kmeans_0.1.csv --file-key INPUT_GENERATOR
  Time (mean ± σ):     843.5 ms ±  48.9 ms    [User: 2590.0 ms, System: 92.3 ms]
  Range (min … max):   794.4 ms … 943.0 ms    10 runs

Benchmark 4: java -Dtinylog.level=trace -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files ../data/adult_random_0.001.csv --file-key INPUT_GENERATOR
  Time (mean ± σ):     718.9 ms ±  24.4 ms    [User: 1871.9 ms, System: 93.6 ms]
  Range (min … max):   687.0 ms … 763.0 ms    10 runs

Benchmark 5: java -Dtinylog.level=trace -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files ../data/adult_random_0.01.csv --file-key INPUT_GENERATOR
  Time (mean ± σ):     615.4 ms ±  22.6 ms    [User: 1556.9 ms, System: 71.7 ms]
  Range (min … max):   587.0 ms … 660.4 ms    10 runs

Benchmark 6: java -Dtinylog.level=trace -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files ../data/adult_random_0.1.csv --file-key INPUT_GENERATOR
  Time (mean ± σ):     693.1 ms ±  33.6 ms    [User: 1858.7 ms, System: 65.6 ms]
  Range (min … max):   657.3 ms … 753.5 ms    10 runs

Benchmark 7: java -Dtinylog.level=trace -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files ../data/adult.csv --file-key INPUT_GENERATOR
  Time (mean ± σ):      1.139 s ±  0.053 s    [User: 4.204 s, System: 0.145 s]
  Range (min … max):    1.069 s …  1.220 s    10 runs

Summary
  'java -Dtinylog.level=trace -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files ../data/adult_random_0.01.csv --file-key INPUT_GENERATOR' ran
    1.06 ± 0.06 times faster than 'java -Dtinylog.level=trace -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files ../data/adult_kmeans_0.01.csv --file-key INPUT_GENERATOR'
    1.13 ± 0.07 times faster than 'java -Dtinylog.level=trace -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files ../data/adult_random_0.1.csv --file-key INPUT_GENERATOR'
    1.13 ± 0.05 times faster than 'java -Dtinylog.level=trace -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files ../data/adult_kmeans_0.001.csv --file-key INPUT_GENERATOR'
    1.17 ± 0.06 times faster than 'java -Dtinylog.level=trace -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files ../data/adult_random_0.001.csv --file-key INPUT_GENERATOR'
    1.37 ± 0.09 times faster than 'java -Dtinylog.level=trace -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files ../data/adult_kmeans_0.1.csv --file-key INPUT_GENERATOR'
    1.85 ± 0.11 times faster than 'java -Dtinylog.level=trace -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files ../data/adult.csv --file-key INPUT_GENERATOR'
```

# Reported time

```shell
$ for f in ../data/*.csv;  echo "=====================================================: $f"; for i in (seq 10); java -Dtinylog.level=info -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files $f --file-key INPUT_GENERATOR | tail -1; end; end
=====================================================: ../data/adult.csv
(metanome-cli) INFO     Elapsed time: 0:00:00.618 (618 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.636 (636 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.592 (592 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.601 (601 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.616 (616 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.591 (591 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.615 (615 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.604 (604 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.596 (596 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.617 (617 ms).
=====================================================: ../data/adult_kmeans_0.001.csv
(metanome-cli) INFO     Elapsed time: 0:00:00.040 (40 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.044 (44 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.038 (38 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.041 (41 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.041 (41 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.047 (47 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.041 (41 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.040 (40 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.042 (42 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.044 (44 ms).
=====================================================: ../data/adult_kmeans_0.01.csv
(metanome-cli) INFO     Elapsed time: 0:00:00.086 (86 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.085 (85 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.094 (94 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.087 (87 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.086 (86 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.095 (95 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.082 (82 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.093 (93 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.086 (86 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.110 (110 ms).
=====================================================: ../data/adult_kmeans_0.1.csv
(metanome-cli) INFO     Elapsed time: 0:00:00.167 (167 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.179 (179 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.162 (162 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.167 (167 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.171 (171 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.185 (185 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.190 (190 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.170 (170 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.161 (161 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.172 (172 ms).
=====================================================: ../data/adult_random_0.001.csv
(metanome-cli) INFO     Elapsed time: 0:00:00.044 (44 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.040 (40 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.049 (49 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.049 (49 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.054 (54 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.049 (49 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.042 (42 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.053 (53 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.043 (43 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.044 (44 ms).
=====================================================: ../data/adult_random_0.01.csv
(metanome-cli) INFO     Elapsed time: 0:00:00.073 (73 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.075 (75 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.074 (74 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.085 (85 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.079 (79 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.088 (88 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.095 (95 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.076 (76 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.070 (70 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.076 (76 ms).
=====================================================: ../data/adult_random_0.1.csv
(metanome-cli) INFO     Elapsed time: 0:00:00.149 (149 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.142 (142 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.147 (147 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.138 (138 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.143 (143 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.144 (144 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.152 (152 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.144 (144 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.153 (153 ms).
(metanome-cli) INFO     Elapsed time: 0:00:00.150 (150 ms).
```

# Output:

```shell
$ for f in ../data/*.csv;  echo "=====================================================: $f"; java -Dtinylog.level=trace -cp metanome-cli-1.2-SNAPSHOT.jar:HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD --files $f --file-key INPUT_GENERATOR; end
=====================================================: ../data/adult.csv
(metanome-cli) TRACE    App.Parameters(algorithmConfigurationValues=[], algorithmClassName=de.metanome.algorithms.hyfd.HyFD, inputDatasetKey=INPUT_GENERATOR, inputDatasets=[../data/adult.csv], pgpassPath=null, dbType=null, inputFileSeparator=;, inputFileQuotechar=", inputFileEscape=, inputFileSkipLines=0, inputFileStrictQuotes=false, inputFileIgnoreLeadingWhiteSpace=false, inputFileHasHeader=false, inputFileSkipDifferingLines=false, inputFileNullString=, tempFileDirectory=null, clearTempFiles=true, clearTempFilesByPrefix=false, output=file)
(metanome-cli) INFO     Running de.metanome.algorithms.hyfd.HyFD
(metanome-cli) INFO     * in:            [../data/adult.csv]
(metanome-cli) INFO     * out:           file
(metanome-cli) INFO     * configuration: []
(metanome-cli) INFO     Initializing algorithm.
(metanome-cli) INFO     Set default value '-1' on requirement 'INPUT_ROW_LIMIT'
(metanome-cli) INFO     Set default value 'true' on requirement 'ENABLE_MEMORY_GUARDIAN'
(metanome-cli) INFO     Set default value 'true' on requirement 'NULL_EQUALS_NULL'
(metanome-cli) INFO     Set default value 'true' on requirement 'VALIDATE_PARALLEL'
(metanome-cli) INFO     Set default value '-1' on requirement 'MAX_DETERMINANT_SIZE'
(metanome-cli) TRACE    Requirement with identifier 'INPUT_GENERATOR' cannot handle default values
(metanome-cli) DEBUG    Execution started at 2022-10-31 23:18:45
Initializing ...
Reading data and calculating plis ...
Sorting plis by number of clusters ...
Inverting plis ...
Extracting integer representations for the records ...
Investigating comparison suggestions ...
Sorting clusters ...(107ms)
Running initial windows ...(68ms)
Moving window over clusters ...
Window signature: [8][2][2][2][2][2][2][2][1][1][1][1][1][1][1]
Inducing FD candidates ...
Validating FDs using plis ...
        Level 0: 1 elements; (V)(C)(G); 0 intersections; 0 validations; 0 invalid; 0 new candidates; --> 0 FDs
        Level 1: 3 elements; (V)(C)(G); 2 intersections; 2 validations; 0 invalid; 0 new candidates; --> 2 FDs
        Level 2: 7 elements; (V)(C)(G); 0 intersections; 0 validations; 0 invalid; 0 new candidates; --> 0 FDs
        Level 3: 19 elements; (V)(C)(G); 0 intersections; 0 validations; 0 invalid; 0 new candidates; --> 0 FDs
        Level 4: 49 elements; (V)(C)(G); 16 intersections; 22 validations; 0 invalid; 0 new candidates; --> 22 FDs
        Level 5: 42 elements; (V)(C)(G); 21 intersections; 25 validations; 0 invalid; 0 new candidates; --> 25 FDs
        Level 6: 25 elements; (V)(C)(G); 9 intersections; 9 validations; 0 invalid; 0 new candidates; --> 9 FDs
        Level 7: 20 elements; (V)(C)(G); 12 intersections; 12 validations; 0 invalid; 0 new candidates; --> 12 FDs
        Level 8: 8 elements; (V)(C)(G); 8 intersections; 8 validations; 0 invalid; 0 new candidates; --> 8 FDs
Translating FD-tree into result format ...
... done! (78 FDs)
Time: 598 ms
(metanome-cli) DEBUG    Execution completed at 2022-10-31 23:18:45
(metanome-cli) INFO     Elapsed time: 0:00:00.598 (598 ms).
=====================================================: ../data/adult_kmeans_0.001.csv
(metanome-cli) TRACE    App.Parameters(algorithmConfigurationValues=[], algorithmClassName=de.metanome.algorithms.hyfd.HyFD, inputDatasetKey=INPUT_GENERATOR, inputDatasets=[../data/adult_kmeans_0.001.csv], pgpassPath=null, dbType=null, inputFileSeparator=;, inputFileQuotechar=", inputFileEscape=, inputFileSkipLines=0, inputFileStrictQuotes=false, inputFileIgnoreLeadingWhiteSpace=false, inputFileHasHeader=false, inputFileSkipDifferingLines=false, inputFileNullString=, tempFileDirectory=null, clearTempFiles=true, clearTempFilesByPrefix=false, output=file)
(metanome-cli) INFO     Running de.metanome.algorithms.hyfd.HyFD
(metanome-cli) INFO     * in:            [../data/adult_kmeans_0.001.csv]
(metanome-cli) INFO     * out:           file
(metanome-cli) INFO     * configuration: []
(metanome-cli) INFO     Initializing algorithm.
(metanome-cli) INFO     Set default value '-1' on requirement 'INPUT_ROW_LIMIT'
(metanome-cli) INFO     Set default value 'true' on requirement 'ENABLE_MEMORY_GUARDIAN'
(metanome-cli) INFO     Set default value 'true' on requirement 'NULL_EQUALS_NULL'
(metanome-cli) INFO     Set default value 'true' on requirement 'VALIDATE_PARALLEL'
(metanome-cli) INFO     Set default value '-1' on requirement 'MAX_DETERMINANT_SIZE'
(metanome-cli) TRACE    Requirement with identifier 'INPUT_GENERATOR' cannot handle default values
(metanome-cli) DEBUG    Execution started at 2022-10-31 23:18:46
Initializing ...
Reading data and calculating plis ...
Sorting plis by number of clusters ...
Inverting plis ...
Extracting integer representations for the records ...
Investigating comparison suggestions ...
Sorting clusters ...(1ms)
Running initial windows ...(2ms)
Moving window over clusters ...
Window signature: [1][3][5][6][3][5][3][5][4][6][3][3][4][10][3]
Inducing FD candidates ...
Validating FDs using plis ...
        Level 0: 1 elements; (V)(C)(G); 0 intersections; 0 validations; 0 invalid; 0 new candidates; --> 0 FDs
        Level 1: 8 elements; (V)(C)(G); 18 intersections; 18 validations; 0 invalid; 0 new candidates; --> 18 FDs
        Level 2: 41 elements; (V)(C)(G); 26 intersections; 45 validations; 0 invalid; 0 new candidates; --> 45 FDs
        Level 3: 103 elements; (V)(C)(G); 89 intersections; 176 validations; 0 invalid; 0 new candidates; --> 176 FDs
        Level 4: 87 elements; (V)(C)(G); 62 intersections; 181 validations; 0 invalid; 0 new candidates; --> 181 FDs
        Level 5: 31 elements; (V)(C)(G); 31 intersections; 99 validations; 0 invalid; 0 new candidates; --> 99 FDs
Translating FD-tree into result format ...
... done! (519 FDs)
Time: 47 ms
(metanome-cli) DEBUG    Execution completed at 2022-10-31 23:18:46
(metanome-cli) INFO     Elapsed time: 0:00:00.047 (47 ms).
=====================================================: ../data/adult_kmeans_0.01.csv
(metanome-cli) TRACE    App.Parameters(algorithmConfigurationValues=[], algorithmClassName=de.metanome.algorithms.hyfd.HyFD, inputDatasetKey=INPUT_GENERATOR, inputDatasets=[../data/adult_kmeans_0.01.csv], pgpassPath=null, dbType=null, inputFileSeparator=;, inputFileQuotechar=", inputFileEscape=, inputFileSkipLines=0, inputFileStrictQuotes=false, inputFileIgnoreLeadingWhiteSpace=false, inputFileHasHeader=false, inputFileSkipDifferingLines=false, inputFileNullString=, tempFileDirectory=null, clearTempFiles=true, clearTempFilesByPrefix=false, output=file)
(metanome-cli) INFO     Running de.metanome.algorithms.hyfd.HyFD
(metanome-cli) INFO     * in:            [../data/adult_kmeans_0.01.csv]
(metanome-cli) INFO     * out:           file
(metanome-cli) INFO     * configuration: []
(metanome-cli) INFO     Initializing algorithm.
(metanome-cli) INFO     Set default value '-1' on requirement 'INPUT_ROW_LIMIT'
(metanome-cli) INFO     Set default value 'true' on requirement 'ENABLE_MEMORY_GUARDIAN'
(metanome-cli) INFO     Set default value 'true' on requirement 'NULL_EQUALS_NULL'
(metanome-cli) INFO     Set default value 'true' on requirement 'VALIDATE_PARALLEL'
(metanome-cli) INFO     Set default value '-1' on requirement 'MAX_DETERMINANT_SIZE'
(metanome-cli) TRACE    Requirement with identifier 'INPUT_GENERATOR' cannot handle default values
(metanome-cli) DEBUG    Execution started at 2022-10-31 23:18:47
Initializing ...
Reading data and calculating plis ...
Sorting plis by number of clusters ...
Inverting plis ...
Extracting integer representations for the records ...
Investigating comparison suggestions ...
Sorting clusters ...(5ms)
Running initial windows ...(6ms)
Moving window over clusters ...
Window signature: [2][12][14][11][6][9][21][4][4][4][6][12][4][3][2]
Inducing FD candidates ...
Validating FDs using plis ...
        Level 0: 1 elements; (V)(C)(G); 0 intersections; 0 validations; 0 invalid; 0 new candidates; --> 0 FDs
        Level 1: 5 elements; (V)(C)(G); 11 intersections; 11 validations; 0 invalid; 0 new candidates; --> 11 FDs
        Level 2: 12 elements; (V)(C)(G); 5 intersections; 20 validations; 0 invalid; 0 new candidates; --> 20 FDs
        Level 3: 22 elements; (V)(C)(G); 3 intersections; 3 validations; 0 invalid; 0 new candidates; --> 3 FDs
        Level 4: 68 elements; (V)(C)(G); 19 intersections; 20 validations; 0 invalid; 0 new candidates; --> 20 FDs
        Level 5: 118 elements; (V)(C)(G); 71 intersections; 86 validations; 2 invalid; 8 new candidates; --> 84 FDs
Investigating comparison suggestions ...
Moving window over clusters ...
Window signature: [2][12][17][20][15][9][23][4][7][5][6][13][4][4][3]
Inducing FD candidates ...
Validating FDs using plis ...
        Level 6: 90 elements; (V)(C)(G); 60 intersections; 66 validations; 0 invalid; 0 new candidates; --> 66 FDs
        Level 7: 41 elements; (V)(C)(G); 41 intersections; 55 validations; 0 invalid; 0 new candidates; --> 55 FDs
Translating FD-tree into result format ...
... done! (259 FDs)
Time: 103 ms
(metanome-cli) DEBUG    Execution completed at 2022-10-31 23:18:47
(metanome-cli) INFO     Elapsed time: 0:00:00.104 (104 ms).
=====================================================: ../data/adult_kmeans_0.1.csv
(metanome-cli) TRACE    App.Parameters(algorithmConfigurationValues=[], algorithmClassName=de.metanome.algorithms.hyfd.HyFD, inputDatasetKey=INPUT_GENERATOR, inputDatasets=[../data/adult_kmeans_0.1.csv], pgpassPath=null, dbType=null, inputFileSeparator=;, inputFileQuotechar=", inputFileEscape=, inputFileSkipLines=0, inputFileStrictQuotes=false, inputFileIgnoreLeadingWhiteSpace=false, inputFileHasHeader=false, inputFileSkipDifferingLines=false, inputFileNullString=, tempFileDirectory=null, clearTempFiles=true, clearTempFilesByPrefix=false, output=file)
(metanome-cli) INFO     Running de.metanome.algorithms.hyfd.HyFD
(metanome-cli) INFO     * in:            [../data/adult_kmeans_0.1.csv]
(metanome-cli) INFO     * out:           file
(metanome-cli) INFO     * configuration: []
(metanome-cli) INFO     Initializing algorithm.
(metanome-cli) INFO     Set default value '-1' on requirement 'INPUT_ROW_LIMIT'
(metanome-cli) INFO     Set default value 'true' on requirement 'ENABLE_MEMORY_GUARDIAN'
(metanome-cli) INFO     Set default value 'true' on requirement 'NULL_EQUALS_NULL'
(metanome-cli) INFO     Set default value 'true' on requirement 'VALIDATE_PARALLEL'
(metanome-cli) INFO     Set default value '-1' on requirement 'MAX_DETERMINANT_SIZE'
(metanome-cli) TRACE    Requirement with identifier 'INPUT_GENERATOR' cannot handle default values
(metanome-cli) DEBUG    Execution started at 2022-10-31 23:18:47
Initializing ...
Reading data and calculating plis ...
Sorting plis by number of clusters ...
Inverting plis ...
Extracting integer representations for the records ...
Investigating comparison suggestions ...
Sorting clusters ...(17ms)
Running initial windows ...(18ms)
Moving window over clusters ...
Window signature: [3][3][2][4][16][4][3][4][6][4][3][2][2][1][2]
Inducing FD candidates ...
Validating FDs using plis ...
        Level 0: 1 elements; (V)(C)(G); 0 intersections; 0 validations; 0 invalid; 0 new candidates; --> 0 FDs
        Level 1: 3 elements; (V)(C)(G); 2 intersections; 2 validations; 0 invalid; 0 new candidates; --> 2 FDs
        Level 2: 11 elements; (V)(C)(G); 2 intersections; 4 validations; 0 invalid; 0 new candidates; --> 4 FDs
        Level 3: 54 elements; (V)(C)(G); 24 intersections; 45 validations; 0 invalid; 0 new candidates; --> 45 FDs
        Level 4: 125 elements; (V)(C)(G); 88 intersections; 184 validations; 0 invalid; 0 new candidates; --> 184 FDs
        Level 5: 105 elements; (V)(C)(G); 87 intersections; 147 validations; 0 invalid; 0 new candidates; --> 147 FDs
        Level 6: 38 elements; (V)(C)(G); 34 intersections; 70 validations; 0 invalid; 0 new candidates; --> 70 FDs
        Level 7: 6 elements; (V)(C)(G); 6 intersections; 12 validations; 0 invalid; 0 new candidates; --> 12 FDs
Translating FD-tree into result format ...
... done! (464 FDs)
Time: 167 ms
(metanome-cli) DEBUG    Execution completed at 2022-10-31 23:18:47
(metanome-cli) INFO     Elapsed time: 0:00:00.167 (167 ms).
=====================================================: ../data/adult_random_0.001.csv
(metanome-cli) TRACE    App.Parameters(algorithmConfigurationValues=[], algorithmClassName=de.metanome.algorithms.hyfd.HyFD, inputDatasetKey=INPUT_GENERATOR, inputDatasets=[../data/adult_random_0.001.csv], pgpassPath=null, dbType=null, inputFileSeparator=;, inputFileQuotechar=", inputFileEscape=, inputFileSkipLines=0, inputFileStrictQuotes=false, inputFileIgnoreLeadingWhiteSpace=false, inputFileHasHeader=false, inputFileSkipDifferingLines=false, inputFileNullString=, tempFileDirectory=null, clearTempFiles=true, clearTempFilesByPrefix=false, output=file)
(metanome-cli) INFO     Running de.metanome.algorithms.hyfd.HyFD
(metanome-cli) INFO     * in:            [../data/adult_random_0.001.csv]
(metanome-cli) INFO     * out:           file
(metanome-cli) INFO     * configuration: []
(metanome-cli) INFO     Initializing algorithm.
(metanome-cli) INFO     Set default value '-1' on requirement 'INPUT_ROW_LIMIT'
(metanome-cli) INFO     Set default value 'true' on requirement 'ENABLE_MEMORY_GUARDIAN'
(metanome-cli) INFO     Set default value 'true' on requirement 'NULL_EQUALS_NULL'
(metanome-cli) INFO     Set default value 'true' on requirement 'VALIDATE_PARALLEL'
(metanome-cli) INFO     Set default value '-1' on requirement 'MAX_DETERMINANT_SIZE'
(metanome-cli) TRACE    Requirement with identifier 'INPUT_GENERATOR' cannot handle default values
(metanome-cli) DEBUG    Execution started at 2022-10-31 23:18:48
Initializing ...
Reading data and calculating plis ...
Sorting plis by number of clusters ...
Inverting plis ...
Extracting integer representations for the records ...
Investigating comparison suggestions ...
Sorting clusters ...(0ms)
Running initial windows ...(2ms)
Moving window over clusters ...
Window signature: [1][3][9][6][3][3][4][3][7][7][6][4][2][2][3]
Inducing FD candidates ...
Validating FDs using plis ...
        Level 0: 1 elements; (V)(C)(G); 0 intersections; 0 validations; 0 invalid; 0 new candidates; --> 0 FDs
        Level 1: 8 elements; (V)(C)(G); 16 intersections; 16 validations; 0 invalid; 0 new candidates; --> 16 FDs
        Level 2: 36 elements; (V)(C)(G); 15 intersections; 32 validations; 0 invalid; 0 new candidates; --> 32 FDs
        Level 3: 112 elements; (V)(C)(G); 74 intersections; 168 validations; 0 invalid; 0 new candidates; --> 168 FDs
        Level 4: 121 elements; (V)(C)(G); 88 intersections; 178 validations; 0 invalid; 0 new candidates; --> 178 FDs
        Level 5: 55 elements; (V)(C)(G); 41 intersections; 52 validations; 0 invalid; 0 new candidates; --> 52 FDs
        Level 6: 20 elements; (V)(C)(G); 15 intersections; 35 validations; 0 invalid; 0 new candidates; --> 35 FDs
        Level 7: 6 elements; (V)(C)(G); 6 intersections; 11 validations; 0 invalid; 0 new candidates; --> 11 FDs
Translating FD-tree into result format ...
... done! (492 FDs)
Time: 45 ms
(metanome-cli) DEBUG    Execution completed at 2022-10-31 23:18:48
(metanome-cli) INFO     Elapsed time: 0:00:00.046 (46 ms).
=====================================================: ../data/adult_random_0.01.csv
(metanome-cli) TRACE    App.Parameters(algorithmConfigurationValues=[], algorithmClassName=de.metanome.algorithms.hyfd.HyFD, inputDatasetKey=INPUT_GENERATOR, inputDatasets=[../data/adult_random_0.01.csv], pgpassPath=null, dbType=null, inputFileSeparator=;, inputFileQuotechar=", inputFileEscape=, inputFileSkipLines=0, inputFileStrictQuotes=false, inputFileIgnoreLeadingWhiteSpace=false, inputFileHasHeader=false, inputFileSkipDifferingLines=false, inputFileNullString=, tempFileDirectory=null, clearTempFiles=true, clearTempFilesByPrefix=false, output=file)
(metanome-cli) INFO     Running de.metanome.algorithms.hyfd.HyFD
(metanome-cli) INFO     * in:            [../data/adult_random_0.01.csv]
(metanome-cli) INFO     * out:           file
(metanome-cli) INFO     * configuration: []
(metanome-cli) INFO     Initializing algorithm.
(metanome-cli) INFO     Set default value '-1' on requirement 'INPUT_ROW_LIMIT'
(metanome-cli) INFO     Set default value 'true' on requirement 'ENABLE_MEMORY_GUARDIAN'
(metanome-cli) INFO     Set default value 'true' on requirement 'NULL_EQUALS_NULL'
(metanome-cli) INFO     Set default value 'true' on requirement 'VALIDATE_PARALLEL'
(metanome-cli) INFO     Set default value '-1' on requirement 'MAX_DETERMINANT_SIZE'
(metanome-cli) TRACE    Requirement with identifier 'INPUT_GENERATOR' cannot handle default values
(metanome-cli) DEBUG    Execution started at 2022-10-31 23:18:49
Initializing ...
Reading data and calculating plis ...
Sorting plis by number of clusters ...
Inverting plis ...
Extracting integer representations for the records ...
Investigating comparison suggestions ...
Sorting clusters ...(4ms)
Running initial windows ...(5ms)
Moving window over clusters ...
Window signature: [2][15][16][5][4][3][27][9][7][10][9][9][3][3][2]
Inducing FD candidates ...
Validating FDs using plis ...
        Level 0: 1 elements; (V)(C)(G); 0 intersections; 0 validations; 0 invalid; 0 new candidates; --> 0 FDs
        Level 1: 4 elements; (V)(C)(G); 7 intersections; 7 validations; 0 invalid; 0 new candidates; --> 7 FDs
        Level 2: 15 elements; (V)(C)(G); 9 intersections; 70 validations; 0 invalid; 0 new candidates; --> 70 FDs
        Level 3: 15 elements; (V)(C)(G); 0 intersections; 0 validations; 0 invalid; 0 new candidates; --> 0 FDs
        Level 4: 42 elements; (V)(C)(G); 4 intersections; 5 validations; 0 invalid; 0 new candidates; --> 5 FDs
        Level 5: 65 elements; (V)(C)(G); 22 intersections; 24 validations; 0 invalid; 0 new candidates; --> 24 FDs
        Level 6: 67 elements; (V)(C)(G); 44 intersections; 53 validations; 0 invalid; 0 new candidates; --> 53 FDs
        Level 7: 30 elements; (V)(C)(G); 28 intersections; 41 validations; 0 invalid; 0 new candidates; --> 41 FDs
        Level 8: 2 elements; (V)(C)(G); 2 intersections; 2 validations; 0 invalid; 0 new candidates; --> 2 FDs
Translating FD-tree into result format ...
... done! (202 FDs)
Time: 81 ms
(metanome-cli) DEBUG    Execution completed at 2022-10-31 23:18:49
(metanome-cli) INFO     Elapsed time: 0:00:00.082 (82 ms).
=====================================================: ../data/adult_random_0.1.csv
(metanome-cli) TRACE    App.Parameters(algorithmConfigurationValues=[], algorithmClassName=de.metanome.algorithms.hyfd.HyFD, inputDatasetKey=INPUT_GENERATOR, inputDatasets=[../data/adult_random_0.1.csv], pgpassPath=null, dbType=null, inputFileSeparator=;, inputFileQuotechar=", inputFileEscape=, inputFileSkipLines=0, inputFileStrictQuotes=false, inputFileIgnoreLeadingWhiteSpace=false, inputFileHasHeader=false, inputFileSkipDifferingLines=false, inputFileNullString=, tempFileDirectory=null, clearTempFiles=true, clearTempFilesByPrefix=false, output=file)
(metanome-cli) INFO     Running de.metanome.algorithms.hyfd.HyFD
(metanome-cli) INFO     * in:            [../data/adult_random_0.1.csv]
(metanome-cli) INFO     * out:           file
(metanome-cli) INFO     * configuration: []
(metanome-cli) INFO     Initializing algorithm.
(metanome-cli) INFO     Set default value '-1' on requirement 'INPUT_ROW_LIMIT'
(metanome-cli) INFO     Set default value 'true' on requirement 'ENABLE_MEMORY_GUARDIAN'
(metanome-cli) INFO     Set default value 'true' on requirement 'NULL_EQUALS_NULL'
(metanome-cli) INFO     Set default value 'true' on requirement 'VALIDATE_PARALLEL'
(metanome-cli) INFO     Set default value '-1' on requirement 'MAX_DETERMINANT_SIZE'
(metanome-cli) TRACE    Requirement with identifier 'INPUT_GENERATOR' cannot handle default values
(metanome-cli) DEBUG    Execution started at 2022-10-31 23:18:49
Initializing ...
Reading data and calculating plis ...
Sorting plis by number of clusters ...
Inverting plis ...
Extracting integer representations for the records ...
Investigating comparison suggestions ...
Sorting clusters ...(16ms)
Running initial windows ...(21ms)
Moving window over clusters ...
Window signature: [3][3][4][12][4][2][3][4][6][3][3][2][2][2][2]
Inducing FD candidates ...
Validating FDs using plis ...
        Level 0: 1 elements; (V)(C)(G); 0 intersections; 0 validations; 0 invalid; 0 new candidates; --> 0 FDs
        Level 1: 3 elements; (V)(C)(G); 2 intersections; 2 validations; 0 invalid; 0 new candidates; --> 2 FDs
        Level 2: 10 elements; (V)(C)(G); 5 intersections; 5 validations; 0 invalid; 0 new candidates; --> 5 FDs
        Level 3: 37 elements; (V)(C)(G); 22 intersections; 44 validations; 0 invalid; 0 new candidates; --> 44 FDs
        Level 4: 59 elements; (V)(C)(G); 53 intersections; 83 validations; 0 invalid; 0 new candidates; --> 83 FDs
        Level 5: 11 elements; (V)(C)(G); 7 intersections; 9 validations; 0 invalid; 0 new candidates; --> 9 FDs
        Level 6: 4 elements; (V)(C)(G); 4 intersections; 9 validations; 0 invalid; 0 new candidates; --> 9 FDs
Translating FD-tree into result format ...
... done! (152 FDs)
Time: 150 ms
(metanome-cli) DEBUG    Execution completed at 2022-10-31 23:18:50
(metanome-cli) INFO     Elapsed time: 0:00:00.151 (151 ms).
```

```r
df <- data.frame(
    mean = c(608.6, 41.8, 80.5, 172.4, 46.7, 79.1, 146.2),
    dev = c(14.25326473, 2.573367875, 24.7980734, 9.524238086, 4.762119043, 7.809538328, 4.802776974),
    fds = c(78, 519, 259, 167, 492, 202, 152),
    dataset = c("Full (78 FDs)", "KMeans 0.1% (519 FDs)", "KMeans 1% (259 FDs)", "KMeans 10% (167 FDs)", "Random 0.1% (492 FDs)", "Random 1% (202 FDs)", "Random 10% (152 FDs)")
)

ggplot(df) +
    geom_bar(aes(x = dataset, y = mean), stat = "identity", fill = "skyblue", alpha = 0.5) +
    ylab("mean runtime of 10 runs in ms") +
    geom_errorbar(aes(x = dataset, ymin = mean - dev, ymax = mean + dev), width = 0.4, colour = "orange", alpha = 0.9, size = 1.3) +
    coord_flip()
```
