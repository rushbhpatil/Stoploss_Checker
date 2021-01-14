from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFlatButton
import sys, time, threading
import pyrebase
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime,timedelta
import pandas_datareader.data as web
from kivymd.theming import ThemeManager
import pandas as pd
from kivymd.icon_definitions import md_icons
from kivy.utils import get_color_from_hex
import webbrowser
from kivymd.uix.screen import Screen
from kivymd.uix.list import MDList,ThreeLineListItem,ThreeLineAvatarIconListItem,OneLineListItem
from kivymd.uix.list import IconLeftWidget,ImageLeftWidget
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivymd.uix.card import MDCardSwipe
from kivy.properties import ObjectProperty
import csv
from os import path
from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ListProperty, BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
import re
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
import pandas as pd
from kivy.clock import Clock
from functools import partial
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField,MDTextFieldRound
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
from kivy.core.window import Window
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


username =''

fg = BooleanProperty(False)
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, MDLabel):
    ''' Add selection support to the Label '''

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    txt_input = ObjectProperty(None)
    stock_name = ObjectProperty(None)
    stock_symbol = ObjectProperty(None)
    purchase_price = ObjectProperty(None)
    stop_loss = ObjectProperty(None)
    highlight = ListProperty([1, 1, 1, 1])

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        rv.clear_selection()
        self.selected = False
        self.index = index

        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):


        ''' Respond to the selection of items in the view. '''

        self.selected = is_selected
        if is_selected:

            # App.get_running_app().root.widget_1.ids.txt_input1.text = str(rv.data[index].get("text"))
            xx =str(rv.data[index].get("text"))
            if (xx.find('(NSI)') != -1):
                x,y = xx.split(" (NSI)")
                add_sym = '.NS'
            else:
                x,y = xx.split(" (BSE)")
                add_sym = '.BO'
            print(xx)
            print(x)

            App.get_running_app().root.get_screen('body_screen').widget_1.ids.stock_name.text = x
            f = pd.read_csv("Stock Tickers.csv", encoding="ISO-8859-1", engine='python')
            fl = len(f.index)
            file = pd.DataFrame(f, columns=['Symbols', 'Name', 'Exchange'])

            for i in range(fl):
                for index in range(1):
                    columnSeriesObj_sym = file.iloc[:, 0]
                    columnSeriesObj1 = file.iloc[:, 1]
                    columnSeriesObj_ex = file.iloc[:, 2]
                    before_sym,b = columnSeriesObj_sym.values[i].split('.')


                    if columnSeriesObj1.values[i] == App.get_running_app().root.get_screen('body_screen').widget_1.ids.stock_name.text:
                        App.get_running_app().root.get_screen('body_screen').widget_1.ids.stock_symbol.text = before_sym + add_sym





class RV(RecycleView):
    def clear_selection(self):
        for c in self.children[0].children:
            c.selected = False



class DropDownWidget(MDBoxLayout):
    txt_input = ObjectProperty(None)
    rv = ObjectProperty(None)
    rv_data_list = ListProperty()
    stock_name = ObjectProperty(None)
    stock_symbol = ObjectProperty(None)
    purchase_price = ObjectProperty(None)
    stop_loss = ObjectProperty(None)
    def back(self):
        self.clear_texts()
        MDApp.get_running_app().root.transition.direction = 'right'
        MDApp.get_running_app().root.current = 'option_screen'
    def clear_texts(self):
        App.get_running_app().root.get_screen('body_screen').widget_1.ids.txt_input.text = ""
        App.get_running_app().root.get_screen('body_screen').widget_1.ids.stock_name.text = ""
        App.get_running_app().root.get_screen('body_screen').widget_1.ids.stock_symbol.text = ""
        App.get_running_app().root.get_screen('body_screen').widget_1.ids.purchase_price.text = ""
        App.get_running_app().root.get_screen('body_screen').widget_1.ids.stop_loss.text = ""

    def sync_file(self):
        updown = Firebaseupdown()
        updown.fire_upload()
        updown.fire_download()
        
        self.clear_texts()

        toast("The data has been synchronized with cloud")
    def btn_input(self):
        global counter
        end = datetime.today().date()
        start = end - timedelta(days=7)

        try:
            if App.get_running_app().root.get_screen('body_screen').widget_1.ids.stock_name.text=='':
                toast(text='Please Select Stock')
            elif App.get_running_app().root.get_screen('body_screen').widget_1.ids.stock_symbol.text=='':
                toast(text='Please Select Stock')
            elif App.get_running_app().root.get_screen('body_screen').widget_1.ids.purchase_price.text=='':
                toast(text='Please Enter Purchase Price')
            elif  App.get_running_app().root.get_screen('body_screen').widget_1.ids.stop_loss.text=='':
                toast(text='Please Enter Stoploss')

            elif float(App.get_running_app().root.get_screen('body_screen').widget_1.ids.stop_loss.text) <= float(App.get_running_app().root.get_screen('body_screen').widget_1.ids.purchase_price.text):

                print("Stock Name:", App.get_running_app().root.get_screen('body_screen').widget_1.ids.stock_name.text,
                      "Stock Symbol:", App.get_running_app().root.get_screen('body_screen').widget_1.ids.stock_symbol.text)
                print("Purchase Price:", App.get_running_app().root.get_screen('body_screen').widget_1.ids.purchase_price.text,
                      "Stop Loss(%):", App.get_running_app().root.get_screen('body_screen').widget_1.ids.stop_loss.text)

                # write data to csv file


                file_name = username +"_stoploss.csv"
                if path.exists(file_name):
                    with open(file_name, "a+", newline='')as newFile:
                        fieldnames = ["Stock Name", "Stock Symbol", "Purchase Price", "Stop Loss(%)"]
                        newFileWriter = csv.DictWriter(newFile, fieldnames=fieldnames)
                        newFileWriter.writerow({"Stock Name": App.get_running_app().root.get_screen('body_screen').widget_1.ids.stock_name.text,
                                                "Stock Symbol": App.get_running_app().root.get_screen('body_screen').widget_1.ids.stock_symbol.text,
                                                "Purchase Price": App.get_running_app().root.get_screen('body_screen').widget_1.ids.purchase_price.text,
                                                "Stop Loss(%)": App.get_running_app().root.get_screen('body_screen').widget_1.ids.stop_loss.text})

                else:
                    myFile = open(file_name, 'w+',newline='')
                    myData = [["Stock Name", "Stock Symbol", "Purchase Price", "Stop Loss(%)"],
                              [App.get_running_app().root.get_screen('body_screen').widget_1.ids.stock_name.text,
                               App.get_running_app().root.get_screen('body_screen').widget_1.ids.stock_symbol.text,
                               App.get_running_app().root.get_screen('body_screen').widget_1.ids.purchase_price.text,
                               App.get_running_app().root.get_screen('body_screen').widget_1.ids.stop_loss.text]]

                    with myFile:
                        writer = csv.writer(myFile)
                        writer.writerows(myData)

                # self.popup = Popup(title='Signing In', content=Image(source='please_wait.gif', size_hint=(1, 1),
                #                                                      pos_hint={'center_x': .5, 'center_y': .5}))
                # self.popup.open()
                threading.Thread(target=self.sync_file()).start()

                counter += 1
            else:
                App.get_running_app().root.get_screen('body_screen').widget_1.ids.stop_loss.text=''
                toast('The Stoloss should be less then Purchase price')
        except ConnectionAbortedError:
            toast("Check your Internet connection")
        except ConnectionRefusedError:
            toast("Check your Internet connection")
        except ConnectionError:
            toast("Check your Internet connection")
        except ConnectionResetError:
            toast("Check your Internet connection")
        except FileNotFoundError:
            toast('File not found')
        except TimeoutError:
            toast('Timeout!!!!...Check your Internet connection')
        except KeyError:
            toast('Some thing went wrong')
            pass
	
class MyTextInput(MDTextFieldRound):
    txt_input = ObjectProperty(None)

    flt_list = ObjectProperty()
    word_list = ListProperty()
    stock_name = ObjectProperty(None)
    stock_symbol = ObjectProperty(None)
    purchase_price = ObjectProperty(None)
    stop_loss = ObjectProperty(None)
    # this is the variable storing the number to which the look-up will start
    starting_no = NumericProperty()
    display_data = ListProperty()
    suggestion_text = ''

    def __init__(self, **kwargs):
        super(MyTextInput, self).__init__(**kwargs)

    def on_text(self, instance, value):
        # find all the occurrence of the word
        app = MDApp.get_running_app()
        print(app.root.ids.body.children[0])  # the dropdown widget
        ddw = app.root.ids.body.children[0]

        ddw.rv_data_list = []
        if len(value) > 0:

            ddw.rv_data_list = [{'text': word} for word in self.word_list if word.lower().find(value.lower()) != -1]

            # ensure the size is okay
            if len(ddw.rv_data_list) <= 10:
                self.parent.height = (50 + (len(ddw.rv_data_list) * 20))
            else:
                self.parent.height = 250

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if self.suggestion_text and keycode[1] == 'tab':
            self.ids.rv.refresh_from_data()
            self.insert_text(self.suggestion_text + ' ')
            return True
        return super(MyTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)


class Body(MDScreen):

    def back(self):
        dw = DropDownWidget()
        dw.clear_texts()
        MDApp.get_running_app().root.transition.direction = 'right'
        MDApp.get_running_app().root.current = 'option_screen'
    def hook_keyboard(self, Window, key, *largs):
        if key == 27:
            self.back()
        return True


    def on_pre_enter (self):
        Window.bind(on_keyboard=self.hook_keyboard)
        f = pd.read_csv("Stock Tickers.csv", encoding = "ISO-8859-1", engine='python')
        fl = len(f.index)
        file = pd.DataFrame(f, columns=['Symbols', 'Name', 'Exchange'])

        wl = []
        for i in range(fl):
            for index in range(1):

                columnSeriesObj = file.iloc[:, 1]
                self.columnSeriesObj_ex = file.iloc[:, 2]


                wl.append(columnSeriesObj.values[i] + " (" + self.columnSeriesObj_ex.values[i] + ")")


        tp = tuple(wl)



        self.widget_1 = DropDownWidget()

        self.widget_1.ids.txt_input.word_list = wl
        self.widget_1.ids.txt_input.starting_no = 3


        self.add_widget(self.widget_1)




class Signin(MDScreen):
    user_name = ObjectProperty(None)

    def hook_keyboard(self, Window, key, *largs):
        if key == 27:
            button_yes = MDFlatButton(text="Ok", text_color=(98 / 255, 0, 238 / 255, 1),
                                     on_press=self.quit_appp)
            button_No = MDFlatButton(text="Ok", text_color=(98 / 255, 0, 238 / 255, 1),
                                      on_press=self.close_dialog1)
            self.signin_dialog = MDDialog(title='Are you sure?', text="This action will close the App",
                                          size_hint=(.9, .5), buttons=[button_No,button_yes])
            self.signin_dialog.open()
        return True

    def quit_appp(self,dl):
        run1().stop()
    def open_link(instance,link):

        webbrowser.open(link)

    def build(self):
        Window.bind(on_keyboard=self.hook_keyboard)

    def check(self,email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        # pass the regular expression
        # and the string in search() method
        if (re.search(regex, email)):
            return True

        else:
            return False


    def btn(self):
        global username
        global fg
        un = self.user_name.text
        if self.check(un):
            username, u = un.split('@')
            print(username)
            fg = True
            # self.popup = Popup(title='Signing In', content=Image(source='please_wait.gif', size_hint=(1, 1),
            #                                                                pos_hint={'center_x': .5, 'center_y': .5}))
            # self.popup.open()
            threading.Thread(target=self.check_fb_file()).start()
        else:
            button_ok = MDFlatButton(text="Ok", text_color=(98 / 255, 0, 238 / 255, 1),
                                          on_press=self.close_dialog)
            self.signin_dialog = MDDialog(title='Error',text="That doesn't appear to be a valid email address",
                                     size_hint=(.9,.5),buttons=[button_ok])
            self.signin_dialog.open()

    def check_fb_file(self):
        down = Firebaseupdown()
        down.fire_download()
        self.user_name.text = ''
        MDApp.get_running_app().root.transition.direction = 'left'
        MDApp.get_running_app().root.current = 'option_screen'
        # self.popup.dismiss()

    def close_dialog(self,obj):
        self.signin_dialog.dismiss()
        self.user_name.text = ''
    def close_dialog1(self,obj):
        self.dialog.dismiss()




counter = 1
class Option(MDScreen):

    global username
    flag_dis = BooleanProperty(False)

    def hook_keyboard(self, Window, key, *largs):
        if key == 27:
            self.back()
        return True



    def build(self, *args):
        global counter

        Window.bind(on_keyboard=self.hook_keyboard)
        file_name = username + "_stoploss.csv"
        if path.exists(file_name) and counter == 1:
            toast("The data has been synchronized with cloud")
            counter += 1

        elif not path.exists(file_name):
            self.flag_dis = True
            toast('Please Go to Add Stock')
        else:
            self.flag_dis = False
            print('All good')
            pass
        

    def back(self):
        MDApp.get_running_app().root.transition.direction = 'right'
        MDApp.get_running_app().root.current = 'signin_screen'

class Firebaseupdown():
    global check1
    config = {
        "apiKey": "AIzaSyAIB1mUIFjjqvopuASTcnr2BiBzonuk_-U",
        "authDomain": "stoploss-795ec.firebaseapp.com",
        "databaseURL": "https://stoploss-795ec.firebaseio.com",
        "projectId": "stoploss-795ec",
        "storageBucket": "stoploss-795ec.appspot.com",
        "messagingSenderId": "262073549430",
        "appId": "1:262073549430:web:d5563e3883cad7e4c59557",
        "measurementId": "G-5STY05PZFK"
    }

    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()

    def fire_upload(self):
        #upload
        try:

            path_on_cloud = username + f"/{username}_stoploss.csv"
            path_local = username +"_stoploss.csv"
            self.storage.child(path_on_cloud).put(path_local)

            check1 = True
        except ConnectionError:
            toast('Please check your Internet connection')
        except ConnectionRefusedError:
            toast('Please check your Internet connection')
        except ConnectionAbortedError:
            toast('Please check your Internet connection')
        except ConnectionResetError:
            toast('Please check your Internet connection')

    def fire_download(self):
        #download
        try:
            downloadlink = username + f"/{username}_stoploss.csv"
            self.storage.child(downloadlink).download(username+'_stoploss.csv')
            self.storage.child(downloadlink).get_url(username+'_stoploss.csv')
        except ConnectionError:
            toast('Please check your Internet connection')
        except ConnectionRefusedError:
            toast('Please check your Internet connection')
        except ConnectionAbortedError:
            toast('Please check your Internet connection')
        except ConnectionResetError:
            toast('Please check your Internet connection')
        except:
            toast('Something went wrong,Please check your Internet connection')





class SwipeToDeleteItem(MDCardSwipe):
    '''Card with `swipe-to-delete` behavior.'''

    text = StringProperty()
    secondary_text = StringProperty()
    tertiary_text = StringProperty()

class Remove_stock(MDScreen):

    text = StringProperty()
    secondary_text = StringProperty()
    tertiary_text = StringProperty()
    inst = None




    def build(self):
        global fg
        Window.bind(on_keyboard=self.hook_keyboard)
        if fg:
            try:

                file_name = username + "_stoploss.csv"
                f = pd.read_csv(file_name)
                file = pd.DataFrame(f, columns=['Stock Name', 'Stock Symbol', 'Purchase Price', 'Stop Loss(%)'])

            except FileNotFoundError:

                self.back()
                toast("File Not found, Please Add stock")


        emptylist_lbl = MDLabel(text='\n\n\n\n\n\nThe List is empty, Please Add Stock Details',
                                pos_hint={'center_x': .5, 'center_y': .5}, halign='center')

        try:
            for name, symbol in zip(file.iloc[:, 0], file.iloc[:, 1]):
                symb,market_name = symbol.split('.')
                if market_name == 'NS':
                    mknm = 'NSE'
                else:
                    mknm = 'BSE'
                item = SwipeToDeleteItem(text=name, secondary_text=symbol,tertiary_text =mknm)
                self.ids.md_list.add_widget(item)
        except UnboundLocalError:
            self.back()
        if len(self.ids.md_list.children)==0:
            self.ids.md_list.add_widget(emptylist_lbl)


    def remove_item_csv(self, txt, sec_txt, instance):
        self.text = txt
        self.secondary_text = sec_txt
        self.inst = instance
        print(f'1: {txt} 2:{sec_txt}')
        print(instance)

        button_cancel = MDFlatButton(text="CANCEL", text_color=(1, 0, 0, 1), on_press=self.close_dialog)
        button_confirm = MDFlatButton(text="CONFIRM", text_color=(98 / 255, 0, 238 / 255, 1),on_press=self.dialog_confirm)

        self.dialog = MDDialog(
            title='Are you sure?',
            text=f"This will remove {txt} from List",
            pos_hint= {'center_x': .5, 'center_y': .5},
            size_hint=(.8,.5),
            buttons=[button_cancel, button_confirm])
        self.dialog.set_normal_height()
        self.dialog.open()

    def dialog_confirm(self, obj):
        global fg
        if fg:
            try:
                file_name = username + "_stoploss.csv"
                f = pd.read_csv(file_name)
                file = pd.DataFrame(f, columns=['Stock Name', 'Stock Symbol', 'Purchase Price', 'Stop Loss(%)'])
            except FileNotFoundError:
                self.back()
                toast("File Not found, Please Add stock")
        try:
            for index, name, symbol in zip(file.index, file.iloc[:, 0], file.iloc[:, 1]):
                if name == self.text and symbol == self.secondary_text:
                    file = file.drop(index, axis=0)
                    print('Stock Removed')

            file.to_csv(file_name, index=False)
            self.ids.md_list.remove_widget(self.inst)

            self.dialog.dismiss()
            self.toast_popup()
            emptylist_lbl = MDLabel(text='\n\n\n\n\n\nThe List is empty, Please Add Stock Details', pos_hint={'center_x':.5,'center_y':.5},halign='center')
            if len(self.ids.md_list.children)==0:
                self.ids.md_list.add_widget(emptylist_lbl)
            updown = Firebaseupdown()
            updown.fire_upload()
            updown.fire_download()
            toast("The data has been synchronized with cloud")
        except ConnectionAbortedError:
            toast("Check your Internet connection")
        except ConnectionRefusedError:
            toast("Check your Internet connection")
        except ConnectionError:
            toast("Check your Internet connection")
        except ConnectionResetError:
            toast("Check your Internet connection")
        except TimeoutError:
            toast('Timeout!!!!...Check your Internet connection')
        except KeyError:
            toast('Some thing went wrong')
            pass
        except FileNotFoundError:
            toast('File not found')

        except:
            toast("Something went wrong")

    def close_dialog(self,obj):
        self.dialog.dismiss()

    def toast_popup(self):
        toast(f'The {self.text} is removed from the list')
    def hook_keyboard(self, Window, key, *largs):
        if key == 27:
            self.back()
        return True

    def back(self):
        MDApp.get_running_app().root.transition.direction = 'right'
        MDApp.get_running_app().root.current = 'option_screen'
        self.ids.md_list.clear_widgets()
class ListApp(MDScreen):
    built = BooleanProperty(False)

    def hook_keyboard(self, Window, key, *largs):
        if key == 27:
            self.back()
        return True
    def update(self):
        self.ids.list_view.clear_widgets()
        self.built = False
        self.build()

    def back(self):
        MDApp.get_running_app().root.transition.direction = 'right'
        MDApp.get_running_app().root.current = 'option_screen'

    def build(self):
        Window.bind(on_keyboard=self.hook_keyboard)
        if self.built:
            return
        self.built = True
        self.popup = Popup(title='Calculating Stoploss', content=Image(source='please_wait.gif',size_hint=(1,1),pos_hint={'center_x':.5,'center_y':.5}))
        self.popup.open()
        threading.Thread(target=self.actual_build).start()

    def actual_build(self):
        global fg
        if fg:
            try:
                file_name = username + "_stoploss.csv"
                f = pd.read_csv(file_name)
                file = pd.DataFrame(f, columns=['Stock Name', 'Stock Symbol', 'Purchase Price', 'Stop Loss(%)'])
                self.fl = len(file.index)
            except UnboundLocalError:
                self.popup.dismiss()
                self.back()
            except FileNotFoundError:
                self.popup.dismiss()
                self.back()
                toast("File Not found, Please Add stock")

        end = datetime.today().date()
        start = end - timedelta(days=7)


        i = 0


        try:
            for index in range(self.fl):

                for index in range(1):
                    columnSeriesObj2 = file.iloc[:, 1]

                    df = web.DataReader(columnSeriesObj2.values[i],'yahoo', start, end,retry_count=3)
                    print(df)
                    print(df.index[-1].date())
                    days = ["Monday", "Tuesday", "Wednesday", "Thursday",
                            "Friday", "Saturday", "Sunday"]
                    print(days[df.index[-1].weekday()])
                    self.weekday_s = days[df.index[-1].weekday()]
                    self.last_date = df.index[-1].date()
                    Objname = file.iloc[:, 0]
                    columnSeriesObj = df.iloc[:, 3]
                    columnSeriesObj1 = file.iloc[:, 3]
                    ObjStoploss = file.iloc[:, 3]


                    pp = iter(columnSeriesObj1.values)

                    cp1 = columnSeriesObj.values[-1]
                    sl = columnSeriesObj1.values[i]
                    print("cp "+str(cp1))
                    print("sl "+str(sl))
                    if cp1 <= sl:
                        Clock.schedule_once(partial(self.add_loss, Objname.values[i], str(cp1), str(sl)))
                        i=i+1
                    else:
                        Clock.schedule_once(partial(self.add_profit, Objname.values[i], str(cp1), str(sl)))
                        i=i+1


        except ConnectionAbortedError:
            toast("Check your Internet connection")
        except ConnectionRefusedError:
            toast("Check your Internet connection")
        except ConnectionError:
            toast("Check your Internet connection")
        except ConnectionResetError:
            toast("Check your Internet connection")

        except TimeoutError:
            toast('Timeout!!!!...Check your Internet connection')
        except KeyError:
            toast('Invaid Symbol')
        except AttributeError:
            pass

        except:
            toast('Something went wrong')

        self.popup.dismiss()


    def add_loss(self, name, close_price, stop_loss, dt):

            image = ImageLeftWidget(source='loss.png')
            date_lbl = OneLineListItem(text=f'Date: {str(self.last_date)}, {self.weekday_s}',size_hint_y=None, height=5)
            items = ThreeLineAvatarIconListItem(text=name, secondary_text='Close price: '+ close_price ,
                                                tertiary_text='Stoploss: ' + stop_loss)
            items.add_widget(image)
            self.ids.list_view.add_widget(date_lbl)
            self.ids.list_view.add_widget(items)

    def add_profit(self, name, close_price, stop_loss, dt):

            image = ImageLeftWidget(source='profit.jpg')
            date_lbl = OneLineListItem(text=f'Date: {str(self.last_date)}, {self.weekday_s}', size_hint_y=None, height=5)
            items = ThreeLineAvatarIconListItem(text=name,
                                                secondary_text='Close price: ' + close_price,
                                                tertiary_text='Stoploss: ' + stop_loss)
            items.add_widget(image)
            self.ids.list_view.add_widget(date_lbl)
            self.ids.list_view.add_widget(items)





sm = ScreenManager()
sm.add_widget(Signin(name='signin_screen'))
sm.add_widget(Option(name='option_screen'))
sm.add_widget(ListApp(name='Stoploss_ip'))
sm.add_widget(Body(name='body_screen'))
sm.add_widget(Remove_stock(name='RemoveStock_screen'))


class run1(MDApp):
    def build(self):
        kv = Builder.load_file("stopl.kv")
        return kv

if __name__ == "__main__":
    run1().run()
