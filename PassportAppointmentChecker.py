from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import smtplib, ssl
from email.mime.text import MIMEText
import random


def send_email():
    print('About to send email notification...')
    port = 465
    email_account = 'reinaldo.otalvaro@gmail.com'
    password = 'CHANGE_PASSWORD'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email_account, password)
        msg = MIMEText('URGENTE CITA JUANK DISPONIBLE PARA PASAPORTE')
        msg['Subject'] = 'URGENTE CITA JUANK DISPONIBLE PARA PASAPORTE'
        msg['From'] = email_account
        msg['To'] = email_account
        server.sendmail(email_account, [email_account], msg.as_string())
        server.quit()


PATH="./chromedriver"
i = 1

#Let's do this forever since I'll never increment "i"...
while i < 5:
    driver = webdriver.Chrome(PATH)
    driver.get("https://tramitesmre.cancilleria.gov.co/tramites/enlinea/agendamiento.xhtml")

    time.sleep(5)
    request_appointment_btn = driver.find_element_by_name("buttonPreSolicitar")
    request_appointment_btn.send_keys(Keys.RETURN)

    time.sleep(5)

    office_select = Select(driver.find_element_by_name('inputOficina:select:entrada'))
    offices = [26, 27, 37] # --> (BTA Calle 100, Calle 53, Centro)
    office_select.select_by_value(str(random.choice(offices))) 

    time.sleep(5)

    procedure_select = Select(driver.find_element_by_name('inputTramite:select:entrada'))
    procedure_select.select_by_value('5') #Regular passport

    time.sleep(5)

    service_select = Select(driver.find_element_by_name('inputServicio:select:entrada'))
    service_select.select_by_value('SOLICITAR') 

    time.sleep(5)

    try:
        error_message = driver.find_element_by_class_name('ui-messages-error-summary').text
        print(error_message)
        message_err = 'No hay citas disponibles'
        if message_err not in error_message:
            print('Aparentemente ya se puede agendar la cita....')
            send_email()
    except NoSuchElementException:
        send_email()
        print('Aparentemente ya se puede agendar la cita....')

    driver.quit()
