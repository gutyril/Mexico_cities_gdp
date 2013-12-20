#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import time

# Url
url = 'http://www.snim.rami.gob.mx/'

try:
	# Init dirver
	driver = webdriver.Firefox()
	driver.get(url)

	# Go to PIB section
	driver.execute_script("javascript:Inicia('tbl_finanzas.php','m'); AgregaPestana({' 2005 ':'fichabasica_fin.php?reporte=pi&tipo=m'});");

	#Get select elements
	options_states_exists = lambda driver: driver.find_element_by_id("estado1").find_elements_by_tag_name("option")
	options_states = WebDriverWait(driver, 30).until(options_states_exists)
	time.sleep(1)
	#Title
	print "Producto interno bruto municipal 2005;"

	#Headers
	print u";;PIB (pesos a precios corrientes de 2005);;PIB per cápita (pesos a precios corrientes de 2005);;".encode('utf-8')
	print u";;En dólares;En pesos;En dólares;En pesos".encode('utf-8')

	# Select all states
	first_state = True
	for state in options_states:
		state_name = state.text
		if first_state:
			first_state = False
		else:
			driver.execute_script("javascript:$('#municipio1').empty();");
			state.click()
		elements_exists = lambda driver: driver.find_element_by_id("municipio1").find_elements_by_tag_name("option")
		cities_options = WebDriverWait(driver, 30).until(elements_exists)
		time.sleep(1)

		first_city = True
		for city in cities_options:
			line = state_name + ";" + city.text + ";"
			if first_city:
				first_city = False
			else:
				driver.execute_script("javascript:$('#datos').empty();")
				city.click()
			
			table_exists = lambda driver: driver.find_element_by_id("datos").find_elements_by_tag_name("table")
			table = WebDriverWait(driver, 30).until(table_exists)
			time.sleep(1)
			tds = table[0].find_elements_by_tag_name("tbody")[0].find_elements_by_tag_name("tr")[0].find_elements_by_tag_name("td")

			# Get data
			for td in tds:
				line = line + td.text + ";"
			print line.encode('utf-8')
finally:
	driver.close()



