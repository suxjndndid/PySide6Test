class buttionFunctionConnect:
    yolo2main_pre_img = Signal(np.ndarray)  # raw image signal
    yolo2main_res_img = Signal(np.ndarray)  # test result signal
    yolo2main_status_msg = Signal(str)  # Detecting/pausing/stopping/testing complete/error reporting signal
    yolo2main_fps = Signal(str)  # fps
    yolo2main_labels = Signal(dict)  # Detected target results (number of each category)
    yolo2main_progress = Signal(int)  # Completeness
    yolo2main_class_num = Signal(int)  # Number of categories detected
    yolo2main_target_num = Signal(int)  # Targets detected