from record import Recorder

def main():
    recorder = Recorder()
    try:
        recorder.start_recording()
        input("Press Enter to stop recording")
    finally:
        recorder.stop_recording()


if __name__=="__main__":
    main()