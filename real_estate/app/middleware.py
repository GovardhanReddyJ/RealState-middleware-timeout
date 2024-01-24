# middleware.py
import threading

class TimeoutMiddleware:
    def __init__(self, get_response, timeout_seconds=10):
        self.get_response = get_response
        self.timeout_seconds = timeout_seconds


    def __call__(self, request):
        response = None
        error = None
        # stop_event = threading.Event()

        def target():
            nonlocal response, error
            try:
                response = self.get_response(request)
            except Exception as e:
                error = e
            # finally:
            #     stop_event.set()  # Set the stop event to indicate completion

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout=self.timeout_seconds)

        if thread.is_alive():
            # stop_event.set()
            # thread.join()  # Wait for the thread to complete after setting the stop event
            # raise TimeoutError(f"Request exceeded {self.timeout_seconds} seconds")
            raise TimeoutError(f"Request exceeded {self.timeout_seconds} seconds")

        if error:
            raise error

        return response
