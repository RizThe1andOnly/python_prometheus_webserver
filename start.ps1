switch ($args[0]) {
    "write" { $runSub = "./log_writer.py"; Break }
    "read" { $runSub = "./log_reader.py"; Break}
    Default {$runSub = "./log_writer.py"; Break}
}

py $runSub