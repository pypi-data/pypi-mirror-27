import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication

from c_gui.start_form import MyGui
'''
Главный скрипт для старта клиента
'''
if __name__ == '__main__':

    # Создаём GUI
    gui = MyGui()
    print(gui.name)

    # Связываем сигнал нажатия кнопки добавить со слотом функцией добавить контакт
    gui.ui.pushAdd.clicked.connect(gui.add_contact)
    gui.ui.pushDel.clicked.connect(gui.del_contact)
    gui.ui.pushAvatar.clicked.connect(gui.file_open_explorer)

    # Получаем юзера по клику в списке контактов
    gui.ui.listWidgetContants.itemClicked.connect(gui.get_user)

    gui.ui.pushBold.clicked.connect(lambda: gui.format('b'))
    gui.ui.pushItalic.clicked.connect(lambda: gui.format('i'))
    gui.ui.pushUnderline.clicked.connect(lambda: gui.format('u'))

    gui.ui.pushSend.clicked.connect(gui.send_message)

    # сигнал мы берем из нашего GuiReciever
    @pyqtSlot(dict)
    def update_chat(data):
        ''' Отображение сообщения в истории
        '''
        try:
            msg = data['text']
            user = data['user']

            current_user = gui.user_to

            # Будем пушить сообщения сначала в словарь
            # Если текущий выбранный юзер совпадает с юзером от которого пришло сообщение
            if current_user == user:
                # То добавляем это сообщение в текущий чат
                gui.ui.textBrowserMessage.append('{}: {}'.format(user, msg))
            # А если юзер не выделен, то пихаем его в словарь
            else:
                # Если уже есть словарь с таким юзером
                if user in gui.messages:
                    gui.messages[user].append('{}: {}'.format(user, msg))
                # Иначе создаём такой словарь
                else:
                    gui.messages[user] = ['{}: {}'.format(user, msg)]
            print(gui.messages)

        except Exception as e:
            print(e)
    gui.listener.gotData.connect(update_chat)

    gui.start_gui()

