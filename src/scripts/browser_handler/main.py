from click import option
import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import traceback
import time


class BrowserHandler:
    '''
    launch_browser(is_headless=False)
        Launches browser for loading source url and scraping

    open_new_page()
        Opens new page in browser and switch focuses to that page

    close_page()
        Closes a page in browser and switches focus to the last page

    '''
    
    def __init__(self) -> None:
        self.opened_page_count = 1
        self.url = ""
        # options = webdriver.ChromeOptions()
        # self.page_handler = webdriver.Chrome(options=options)

    def launch_browser(self, is_headless=False) -> None:
        is_local_run = True if 'LOCAL_RUN' in os.environ and os.environ["LOCAL_RUN"] else False

        # chrome is set default_browser
        #options.add_argument('--headless') 
        options = webdriver.ChromeOptions()
        self.page_handler = webdriver.Chrome(options=options)
        return self.page_handler


    def open_new_page(self) -> None:
        '''Opens new page in browser and switch focuses to that page'''

        self.opened_page_count += 1
        self.page_handler.execute_script("window.open('');")
        self.page_handler.switch_to.window(self.page_handler.window_handles[-1])

    def close_page(self) -> None:
        '''Closes a page in browser and switches focus to the last page'''

        self.page_handler.close()
        self.page_handler.switch_to.window(self.page_handler.window_handles[-1])

    def close_belated_open_pages(self, main_page_handle) -> None:
        '''closing old page and handling new opened page'''
        
        page_handles_list = self.page_handler.window_handles
        if main_page_handle in page_handles_list:
            main_page_handle_index = page_handles_list.index(main_page_handle)
            for page_handle in page_handles_list[main_page_handle_index + 1 :]:
                self.page_handler.switch_to.window(page_handle)
                self.close_page()
        else:
            raise "Problem with close_belated_open_pages()"


