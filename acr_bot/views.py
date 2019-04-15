from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from json import loads
from multiprocessing import Queue, Process
from acr_bot.bot.bot import process_updates

q = Queue()
flag = True


@csrf_exempt
def handle_request(request):
    """
    Handles POST request to ACR_bot.
    Spawn multiple processes for simultaneous updates processing.
    :param request: POST request from Telegram servers.
    :return: HTTP code 200 'ok'.
    """
    global flag

    if request.method == 'POST':
        json = loads(request.body)
        q.put(json)

        if flag:
            flag = False
            processes = [Process(target=process_updates, args=(q,)) for _ in range(4)]

            for process in processes:
                process.start()
                print(f'{process.name} started')

            for process in processes:
                process.join()
                print(f'{process.name} stopped')
    return HttpResponse('')



