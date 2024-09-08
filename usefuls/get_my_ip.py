IP_PROVIDERS = (
    'checkip.amazonaws.com',
    'icanhazip.com',
    'ifconfig.me',
    'eth0.me',
    'api.ipify.org',
)

def get_my_ip(ip_providers: tuple[str, ...] | None = None):

    import http.client
    from socket import gaierror

    ip_providers = ip_providers or IP_PROVIDERS

    def read_http(provider_host_url: str) -> str:
        http_connection = http.client.HTTPSConnection(provider_host_url)
        try:
            http_connection.request('GET', '/')
        except (http.client.HTTPException, gaierror):
            return ''

        provider_http_response = http_connection.getresponse()

        return provider_http_response.read().decode('utf-8').rstrip()

    ip_got = ''
    providers = iter(ip_providers)

    while not ip_got:
        provider = next(providers)
        ip_got = read_http(provider)

    return ip_got

if __name__ == '__main__':
    get_my_ip()
