from sys import executable
import time
import os
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent



PROXY_HOST = ''
PROXY_PORT = ''
PROXY_USER = ''
PROXY_PASS = ''

manifest_json = """
{
    'version': '1.0.0',
    'manifest_version': 2,
    'name': 'Chrome Proxy',
    'permissions': [
        'proxy',
        'tabs',
        'unlimitedStorage',
        'storage',
        '<all_urls>',
        'webRequest',
        'webRequestBlocking'
    ],
    'background': {
        'scripts: ['background.js']
    },
    'minimum_chrome_version':'76.0.0'
}
"""

background_js = '''
let config = {
        mode: 'fixed_servers',
        rules: {
        SingleProxy: {
            scheme: 'http',
            host: '%s',
            port: parseInt(%s)
        },
        bypassList: ['localhost']
        }
    };
chrome.proxy.settings.set({value: config, scope: 'regular'}, function() {});
function callbackFn(details) {
    return {
        authCredentails: {
            username: '%s',
            password: '%s'
        }
    };
}
chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ['<all_urls>']},
            ['blocking']
);
''' % (PROXY_HOST, PROXY_PASS, PROXY_PORT, PROXY_USER)

def get_chromedriver(use_proxy=False, user_agent=None):
    chrome_options = webdriver.ChromeOptions()
    
    if use_proxy:
        plugin_file = 'proxy_auth_plugin.zip'
        
        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr('monifest.json', manifest_json)
            zp.writestr('background.js', background_js)
            
        chrome_options.add_extension(plugin_file)
        
    if user_agent:
        chrome_options.add_argument(f'--user-agent={user_agent}')
            
            
    s = Service(
        executable_path='chromedriver.exe'
    )
    
    driver = webdriver.Chrome(
        service=s,
        options=chrome_options
    )
    driver.maximize_window

    return driver

    

def main():
    driver = get_chromedriver(use_proxy=True)
    driver.get('https://kick.com')
    time.sleep(10)
    driver.close()
    driver.quit()
    
    
if __name__ == '__main__':
    main()