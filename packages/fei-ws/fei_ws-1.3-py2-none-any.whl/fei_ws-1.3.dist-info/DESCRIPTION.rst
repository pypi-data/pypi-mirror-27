======
fei-ws
======

Wrapper for the federation Equestre Internationale(FEI) Results Provider Web Service.
Works both with and without Django.

Both the old and new versions of the FEI web services are implemented.
They are known as FEIWSClient10 (old) and FEIWSClient(new).
To use the clients supply your username and password when initializing the object or set FEI_WS_USERNAME and FEI_WS_PASSWORD in django config.
Data is returned, as is. No interpretation except for minor exception handling is used on the responses.


