# -*- coding: utf-8 -*- 
# First things, first. Import the wxPython package.

import os
import os.path 
#join, getsize, isfile, getatime, getctime, getmtime, exists, isdir
import shutil
import time
from ctypes import windll
from threading import Thread
from win32api import GetModuleFileName, GetModuleHandle

try:
	import wx
	import wx.lib.mixins.listctrl  as  listmix
except ImportError:
	"""
	try:
		os.system('python3 -m pip install --proxy 172.31.0.14:6588 wxPython')
	except:
		pass
	try:
		os.system('python -m pip install --proxy 172.31.0.14:6588 wxPython')
	except:
		pass

	import wx
	import wx.lib.mixins.listctrl  as  listmix
	"""
	print('Fail with import, exit')
	exit()


class ProListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ColumnSorterMixin): #listmix.ListRowHighlighter
	"""
		Lista ordenable
	"""
	def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.LC_REPORT|wx.BORDER_SUNKEN, columnas = 2):
		wx.ListCtrl.__init__(self, parent, id, pos, size, style)
		listmix.ListCtrlAutoWidthMixin.__init__(self)
		listmix.ColumnSorterMixin.__init__(self, columnas)
		#listmix.ListRowHighlighter.__init__(self, color=None, mode=listmix.HIGHLIGHT_EVEN)
		self.itemDataMap = {}
	def GetListCtrl(self):
		return self

class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin, listmix.ListCtrlAutoWidthMixin, listmix.ColumnSorterMixin): #listmix.ListRowHighlighter
	"""
		Lista editable
	"""
	def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.LC_REPORT|wx.BORDER_SUNKEN, columnas = 2):
		"""Constructor"""
		wx.ListCtrl.__init__(self, parent, id, pos, size, style)
		listmix.TextEditMixin.__init__(self)
		listmix.ListCtrlAutoWidthMixin.__init__(self)
		listmix.ColumnSorterMixin.__init__(self, columnas)
		#listmix.ListRowHighlighter.__init__(self, color=None, mode=listmix.HIGHLIGHT_EVEN)
		self.itemDataMap = {}
	def GetListCtrl(self):
		return self

class OtherFrame(wx.Frame):
    """
    Class used for creating frames other than the main one
    """
    def __init__(self, title, parent=None):
    	style = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER)
    	wx.Frame.__init__(self, parent=parent, title=title, style = style)
    	self.SizerPrincipal = wx.BoxSizer(wx.VERTICAL)
    	self.Show()

class wxCommander(wx.Frame):
	def __init__(self):
		title = 'wxCommander'
		#style = wx.DEFAULT_FRAME_STYLE & ~ (wx.FRAME_NO_TASKBAR) & wx.STAY_ON_TOP & ~ (wx.RESIZE_BORDER)
		style = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER)
		wx.Frame.__init__(self,parent=None, title=title, style=style, size = (1920,1080))
		self.Maximize(True)
		#self.SetSize(1920, 1080)
		self.panelHijo = MyPanel(self)
		self.frame_number = 1

		#self.Maximize(True)
		self.SizerPrincipal = wx.BoxSizer(wx.VERTICAL)
		self.SizerPrincipal.Add(self.panelHijo, 1, wx.EXPAND)
		self.Bind(wx.EVT_SIZE, self.OnResizeWindow)
		# Evento de foco
		#self.Bind(wx.EVT_SET_FOCUS, self.onFocus)
		#self.panelHijo.Bind(wx.EVT_LEFT_UP, self.OnLeftClick)
		#self.panelHijo.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
		#self.panelHijo.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
		#self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
		self.SetSizer(self.SizerPrincipal)
		try:
			if os.path.isfile('icono.ico'):
				icono = wx.Icon("icono.ico")
			else:
				exeName = GetModuleFileName(GetModuleHandle(None))
				icono = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
			self.SetIcon(icono)
		except:
			pass

		self.__barraMenus()
		self.CreateStatusBar()
		self.SetStatusText("Copyright TOI")
		#self.Fit()
		self.Show()

	def on_new_frame(self, event = None):
		if event is None:
			title = 'Busqueda'
		else:
			title = 'SubFrame {}'.format(self.frame_number)
		frame = OtherFrame(title=title, parent = self)
		self.frame_number += 1

	def __barraMenus(self):
		#Creacion de un menu / seria la plantilla del menu, posteriormente se "ubica"
		self.wdMenu = wx.Menu()

		# Añadimos objetos al menu
		# "\t..." Asigna combinacion de teclas para activar el evento del menus
		self.openFolderMenuItem1 = self.wdMenu.Append(1, 'Selecciona carpeta 1\tCtrl-1', 'Selecciona carpeta')
		self.openFolderMenuItem2 = self.wdMenu.Append(2, 'Selecciona carpeta 2\tCtrl-2', 'Selecciona carpeta')
		self.wdMenu.AppendSeparator()
		self.searchItem = self.wdMenu.Append(3, 'Buscar..\tCtrl-B')
		self.exitItem = self.wdMenu.Append(-1, '&Exit\tCtrl-Q')

		#Creacion de otro menu / seria la plantilla del menu, posteriormente se "ubica"
		self.helpMenu = wx.Menu()

		# Añadimos objeto al menu
		self.aboutItem = self.helpMenu.Append(4, 'Informacion\tF1')

		# Creamos la barra para ubicar el menu y añadimos los menus
		self.menuBar = wx.MenuBar()
		self.menuBar.Append(self.wdMenu, "&Menu")
		self.menuBar.Append(self.helpMenu, "&Ayuda")

		# Activamos/asignamos la barra de menu
		self.SetMenuBar(self.menuBar)

		
		#Vinculamos los menus a los metodos correspondientes en base a eventos
		self.Bind(wx.EVT_MENU, self.OnOpenFolder, self.openFolderMenuItem1)
		self.Bind(wx.EVT_MENU, self.OnOpenFolder, self.openFolderMenuItem2)
		self.Bind(wx.EVT_MENU, self.OnExit, self.exitItem)
		self.Bind(wx.EVT_MENU, self.OnBuscar, self.searchItem)
		self.Bind(wx.EVT_MENU, self.OnAbout, self.aboutItem)

	def OnOpenFolder(self, event):
		idEvento = event.GetId()
		#print('Id %d en el evneto en OnOpenFolder' % idEvento)
		rutas = ['U:\\Profile\\Mis documentos\\TOI','C:\\Users\\bvf1426\\Desktop\\TOI', 'U:\\Profile\\Mis documentos', 'C:\\Users','c:\\', 'k:\\']
		if idEvento == 1:
			if os.path.exists(rutas[0]):
				rutaDefecto = rutas[0]
			else:
				rutaDefecto = rutas[4]
		elif idEvento == 2:
			if os.path.exists(rutas[1]):
				rutaDefecto = rutas[1]
			else:
				rutaDefecto = rutas[5]

		#print(event.GetEventObject())
		#print(event.GetEventObject().GetLabel())
		#print(event.EventObject.GetLabel())
		#dlg = wx.DirDialog (self, "Choose input directory", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
		self.dlg = wx.DirDialog(None, "Selecciona directorio para trabajar", rutaDefecto, wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST| wx.DIALOG_NO_PARENT)
		#self.dlg = wx.FileDialog(None, message="Choose a Python file", defaultDir=os.getcwd(),defaultFile="", wildcard=wildcard, style=wx.FD_OPEN)
		try:
			resultado = self.dlg.ShowModal()
			if resultado == wx.ID_OK:
				if idEvento == 1:
					self.panelHijo.path = self.dlg.GetPath()
				elif idEvento == 2:
					self.panelHijo.path2 = self.dlg.GetPath()
				else:
					print(idEvento)
					return False
			else:
				return False
		except Exception:
			wx.LogError('Failed to open directory!')
			raise
		finally:
			self.dlg.Destroy()

		self.panelHijo.refrescarLista(modo = idEvento)

	def OnResizeWindow(self, event):
		event.Skip()
		if not self.IsMaximized():
			self.Update()
		else:
			self.SizerPrincipal.Layout()

	def OnExit(self, event):
		"""Metodo asociado al evento de cierre de la ventana."""
		self.Close(True)

	def OnAbout(self, event):
		"""Metodo asociado al evento vinculado al menu aboutItem"""
		wx.MessageBox('\nAplicacion que te permite explorar dos estructuras de archivos\nseparadas y trabajar con ellas.\nFiltra para trabajar unicamente con archivos .py.\nSe pueden copiar archivos de un panel al otro con dobleclick y \nse pueden borrar  con la tecla supr.\nHay un menu contextual con mas opciones.\nEl panel izquierdo esta "protegido",\npide confirmacion para sobreescribir.',
					  "Breve ayuda",
					  wx.OK|wx.ICON_INFORMATION)

	def OnBuscar(self,event):
		#print('Buscar')
		#print(self.panelHijo.enfocado)
		if self.panelHijo.enfocado in [1,2,3,4]:
			__dicc = {1:'Panel directorio 1', 2:'Panel directorio 2', 3:'Panel archivos 1', 4:'Panel archivos 2'}
			dlg = wx.TextEntryDialog(self, 'Buscar', 'Busqueda en %s' % __dicc[self.panelHijo.enfocado] )
			dlg.ShowModal()
			resultado = ''
			resultado = dlg.GetValue()
			dlg.Destroy()
			if resultado and resultado != '':
				self.panelHijo.buscarLista(resultado)
		#self.on_new_frame()

	def onFocus(self, event):
		print('onfoco')
		print(event.GetId())

	def OnDisable(self, event):
		self.menuBar.EnableTop(0, False)

	def OnRightClick(self, event):
		print(event.GetId())
		print('OrcPapa')
	
	def OnLeftClick(self, event):
		print(event.GetId())
		print('OlcPapa')

class MyPanel(wx.Panel):
	def __init__(self,parent):
		wx.Panel.__init__(self,parent)
		self.__parent = parent
		# (1280, 1024)
		# (1920, 1080)
		self.resolucion = self.__resolucion()
		self.__size = (1920, 1080) if self.resolucion[1] == 1080 else (1280, 1024)
		#self.__parent.SetSize(self.__size)
		self.__parent.SetSize(self.resolucion)
		self.enfocado = 0

		#self.path = self.path2 = os.getcwd()
		#self.path = 'U:\\Profile\\Mis documentos\\TOI'
		#self.path2 = 'C:\\Users\\bvf1426\\Desktop\\TOI'
		self.path = ''
		self.path2 = ''
		self.__listaEditable = [False, False, False, False]
		self.__listaFiltrada = [False, False]
		self.__iniciarObjetos()
		
	def __iniciarObjetos(self):
		# Inicializmos panel y sizers para ubicacion de objetos
		
		self.__crearSizers()

		self.__crearEtiquetas()

		self.__crearListas()

		self.__montarPaneles()

		self.__vincularEventos()	

	def __vincularEventos(self):
		# Vinculamos evento a las etiquetas
		self.st00.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
		self.st01.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
		self.st10.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
		self.st11.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)

		# Vinculamos evento de las listas al metodo correspondiente
		self.list_ctrl00.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
		self.list_ctrl01.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
		self.list_ctrl02.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
		self.list_ctrl03.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)

		self.list_ctrl00.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnList)
		self.list_ctrl01.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnList)
		self.list_ctrl02.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnList)
		self.list_ctrl03.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnList)

		self.list_ctrl00.Bind(wx.EVT_SET_FOCUS, self.onFocus)
		self.list_ctrl01.Bind(wx.EVT_SET_FOCUS, self.onFocus)
		self.list_ctrl02.Bind(wx.EVT_SET_FOCUS, self.onFocus)
		self.list_ctrl03.Bind(wx.EVT_SET_FOCUS, self.onFocus)

		self.list_ctrl00.Bind(wx.EVT_LIST_KEY_DOWN, self.OnPressKey)
		self.list_ctrl01.Bind(wx.EVT_LIST_KEY_DOWN, self.OnPressKey)
		self.list_ctrl02.Bind(wx.EVT_LIST_KEY_DOWN, self.OnPressKey)
		self.list_ctrl03.Bind(wx.EVT_LIST_KEY_DOWN, self.OnPressKey)

		#self.Bind(wx.EVT_KEY_UP, self.OnReleaseKey)

		self.list_ctrl00.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnMouseRight)
		self.list_ctrl01.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnMouseRight)
		self.list_ctrl02.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnMouseRight)
		self.list_ctrl03.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnMouseRight)


		self.list_ctrl00.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.OnRightClick)
		self.list_ctrl01.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.OnRightClick)
		self.list_ctrl02.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.OnRightClick)
		self.list_ctrl03.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.OnRightClick)

		#self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick, self.list_ctrl01)

		self.list_ctrl00.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnUpdateItem)
		self.list_ctrl01.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnUpdateItem)
		self.list_ctrl02.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnUpdateItem)
		self.list_ctrl03.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnUpdateItem)

		self.list_ctrl00.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelected)
		self.list_ctrl01.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelected)
		self.list_ctrl02.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelected)
		self.list_ctrl03.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelected)

		if self.__listaEditable[0]:
			#print('Unbind')
			self.list_ctrl00.Unbind(wx.EVT_LIST_ITEM_SELECTED)
		if self.__listaEditable[1]:
			#print('Unbind')
			self.list_ctrl02.Unbind(wx.EVT_LIST_ITEM_SELECTED)

		if self.__listaEditable[2]:
			#print('Unbind')
			self.list_ctrl01.Unbind(wx.EVT_LIST_ITEM_SELECTED)
		if self.__listaEditable[3]:
			#print('Unbind')
			self.list_ctrl03.Unbind(wx.EVT_LIST_ITEM_SELECTED)


		#self.Bind(wx.EVT_KEY_DOWN, self.OnPressKey)
		#self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
		self.Bind(wx.EVT_LEFT_UP, self.OnSelected)
		self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.list_ctrl01)
		self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.list_ctrl03)

	def __crearSizers(self):
		self.sizerh00 = wx.BoxSizer(wx.HORIZONTAL)

		self.sizerv1 = wx.BoxSizer(wx.VERTICAL)
		self.sizerv2 = wx.BoxSizer(wx.VERTICAL)
		
		self.sizerh1 = wx.BoxSizer(wx.HORIZONTAL)
		self.sizerh2 = wx.BoxSizer(wx.HORIZONTAL)
		self.sizerh3 = wx.BoxSizer(wx.HORIZONTAL)
		self.sizerh4 = wx.BoxSizer(wx.HORIZONTAL)

	def __crearEtiquetas(self):
		# Creacion de etiquetas
		self.st00 = wx.StaticText(self, label="Selecciona ruta")
		font = self.st00.GetFont()
		font.PointSize += 2
		font = font.Bold()
		self.st00.SetFont(font)

		self.st01 = wx.StaticText(self, label='Unidad sin asignar')
		font = self.st01.GetFont()
		font.PointSize += 3
		font = font.Bold()
		self.st01.SetFont(font)

		self.st10 = wx.StaticText(self, label="Selecciona ruta")
		font = self.st10.GetFont()
		font.PointSize += 2
		font = font.Bold()
		self.st10.SetFont(font)

		self.st11 = wx.StaticText(self, label='Unidad sin asignar')
		font = self.st11.GetFont()
		font.PointSize += 3
		font = font.Bold()
		self.st11.SetFont(font)

	def __crearListas(self):
		# Creacion de listas
		self.__colors = []
		#__colorPro = (247, 248, 249)
		__colorPro = (250, 230, 222)
		__colorPro = (233, 251, 245)
		#__colorEdit = (249, 202, 130)
		
		__colorEdit = (236, 212, 173)
		__colorEdit = (196, 252, 233)

		__colorPro = (236, 252, 255)
		#__colorEdit = (62, 100, 255)
		__colorEdit = (138, 160, 255)

		if self.__listaEditable[0]:
			self.list_ctrl00 = EditableListCtrl(self, id = 10, style=wx.LC_REPORT | wx.BORDER_SUNKEN, columnas = 1)
			self.__colors.append(__colorEdit)
		else:
			self.list_ctrl00 = ProListCtrl(self, id = 10, style=wx.LC_REPORT | wx.BORDER_SUNKEN, columnas = 1)
			self.__colors.append(__colorPro)


		if self.__listaEditable[2]:	
			self.list_ctrl01 = EditableListCtrl(self, id = 30, style=wx.LC_REPORT | wx.BORDER_SUNKEN, columnas = 2)
			self.__colors.append(__colorEdit)
		else:
			self.list_ctrl01 = ProListCtrl(self, id = 30, style=wx.LC_REPORT | wx.BORDER_SUNKEN, columnas = 2)
			self.__colors.append(__colorPro)


		if self.__listaEditable[1]:
			self.list_ctrl02 = EditableListCtrl(self, id = 20, style=wx.LC_REPORT | wx.BORDER_SUNKEN, columnas = 1)
			self.__colors.append(__colorEdit)
		else:
			self.list_ctrl02 = ProListCtrl(self, id = 20, style=wx.LC_REPORT | wx.BORDER_SUNKEN, columnas = 1)
			self.__colors.append(__colorPro)


		if self.__listaEditable[3]:
			self.list_ctrl03 = EditableListCtrl(self, id = 40, style=wx.LC_REPORT | wx.BORDER_SUNKEN, columnas = 2)
			self.__colors.append(__colorEdit)
		else:			
			self.list_ctrl03 = ProListCtrl(self, id = 40, style=wx.LC_REPORT | wx.BORDER_SUNKEN, columnas = 2)
			self.__colors.append(__colorPro)
		

		# Color de fondo
		self.list_ctrl00.SetBackgroundColour(self.__colors[0])
		self.list_ctrl01.SetBackgroundColour(self.__colors[1])
		self.list_ctrl02.SetBackgroundColour(self.__colors[2])
		self.list_ctrl03.SetBackgroundColour(self.__colors[3])

		# Insercion de columnas
		self.list_ctrl00.InsertColumn(0, 'Directorios', width=wx.LIST_AUTOSIZE_USEHEADER)
		self.list_ctrl01.InsertColumn(0, 'Archivos', width=wx.LIST_AUTOSIZE_USEHEADER)
		self.list_ctrl02.InsertColumn(0, 'Directorios', width=wx.LIST_AUTOSIZE_USEHEADER)
		self.list_ctrl03.InsertColumn(0, 'Archivos', width=wx.LIST_AUTOSIZE_USEHEADER)


		# Modifacion de fuente
		self.list_ctrl00.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
		self.list_ctrl01.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
		self.list_ctrl02.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
		self.list_ctrl03.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL))

	def __montarPaneles(self):
		__margen = 170 if self.resolucion[1] == 1080 else 90
		# Montamos estructura con los sizers
		self.sizerh1.Add(self.st00,1, wx.ALL, 5)	
		self.sizerh1.Add(self.st01,1, wx.LEFT, __margen)
		#self.sizerh1.Add(self.st01,1, wx.ALIGN_RIGHT, 0)

		self.sizerh2.Add(self.st10, 1, wx.ALL, 5)
		self.sizerh2.Add(self.st11, 1, wx.LEFT, __margen)

		self.sizerh3.Add(self.list_ctrl00,1, wx.EXPAND, 0)
		self.sizerh3.Add(self.list_ctrl01,1, wx.EXPAND, 0)

		self.sizerh4.Add(self.list_ctrl02,1, wx.EXPAND, 0)
		self.sizerh4.Add(self.list_ctrl03,1, wx.EXPAND, 0)

		self.sizerv1.Add(self.sizerh1,0,0, 0)
		self.sizerv1.Add(self.sizerh3,1,wx.EXPAND, 0)

		self.sizerv2.Add(self.sizerh2,0,0, 0)
		self.sizerv2.Add(self.sizerh4,1,wx.EXPAND, 0)

		self.sizerh00.Add(self.sizerv1,1,wx.EXPAND, 0)
		self.sizerh00.Add(self.sizerv2,1,wx.EXPAND, 0)

		self.SetSizer(self.sizerh00)

	def __vaciarPaneles(self):
		self.sizerv1.Hide(self.sizerh3)
		self.sizerv1.Remove(self.sizerh3)
		self.sizerv1.Hide(self.sizerh1)
		self.sizerv1.Remove(self.sizerh1)
		self.__parent.SizerPrincipal.Layout()
		#self.__parent.Fit()
		
		self.sizerv2.Hide(self.sizerh4)
		self.sizerv2.Remove(self.sizerh4)
		self.sizerv2.Hide(self.sizerh2)
		self.sizerv2.Remove(self.sizerh2)
		self.__parent.SizerPrincipal.Layout()
		#self.__parent.Fit()
		
		self.sizerh00.Hide(self.sizerv1)
		self.sizerh00.Remove(self.sizerv1)

		self.sizerh00.Hide(self.sizerv2)
		self.sizerh00.Remove(self.sizerv2)
		self.__parent.SizerPrincipal.Layout()
		#self.__parent.Fit()

	def __refrescarLista(self, modo = 1, buscar = False):
		#print('Modo %d de edicion en lista' % modo)
		__buscar = False
		if self.resolucion[1] == 1080:
			__textoBase = 'Trabajando en unidad %s:\\'
			__maxC = 65
		else:
			__textoBase = 'Trabajando en %s:\\'
			__maxC = 40
		if modo == 1:
			self.list_ctrl00.ClearAll()
			self.list_ctrl01.ClearAll()

			self.list_ctrl00.SetBackgroundColour(self.__colors[0])
			self.list_ctrl01.SetBackgroundColour(self.__colors[1])

			self.list_ctrl00.InsertColumn(0, 'Directorios', width=wx.LIST_AUTOSIZE_USEHEADER)
			self.list_ctrl01.InsertColumn(0, 'Archivos', width=wx.LIST_AUTOSIZE)
			self.list_ctrl01.InsertColumn(1, 'Modificado', width=wx.LIST_AUTOSIZE)

			if self.path != '':
				aux = self.path
				contador = 1
				while len(aux) > __maxC:
					if contador == 5:
						break
					aux = aux.split('\\')
					aux[contador] = '..'
					aux = '\\'.join(aux)
					contador += 1

				self.st00.SetLabel(aux)
				if self.__listaFiltrada[0]:
					__textoBase += '    Filtro (.py)'
				self.st01.SetLabel(__textoBase % self.path[0])
			__path = self.path
			self.list_ctrl00.itemDataMap = {}
			self.list_ctrl01.itemDataMap = {}
			objetoD = self.list_ctrl00
			objetoF = self.list_ctrl01
			
			if buscar:
				if self.enfocado == 1:
					__buscar = 'D'
				elif self.enfocado == 3:
					__buscar = 'A'

		elif modo == 2:
			self.list_ctrl02.ClearAll()
			self.list_ctrl03.ClearAll()

			self.list_ctrl02.SetBackgroundColour(self.__colors[2])
			self.list_ctrl03.SetBackgroundColour(self.__colors[3])
			
			self.list_ctrl02.InsertColumn(0, 'Directorios', width=wx.LIST_AUTOSIZE_USEHEADER)
			self.list_ctrl03.InsertColumn(0, 'Archivos', width=wx.LIST_AUTOSIZE)
			self.list_ctrl03.InsertColumn(1, 'Modificado', width=wx.LIST_AUTOSIZE)

			if self.path2 != '':
				aux = self.path2
				contador = 1
				while len(aux) > __maxC:
					if contador == 5:
						break
					aux = aux.split('\\')
					aux[contador] = '..'
					aux = '\\'.join(aux)
					contador += 1

				self.st10.SetLabel(aux)
				if self.__listaFiltrada[1]:
					__textoBase += '    Filtro (.py)'
				self.st11.SetLabel(__textoBase % self.path2[0])
			__path = self.path2

			self.list_ctrl02.itemDataMap = {}
			self.list_ctrl03.itemDataMap = {}

			objetoD = self.list_ctrl02
			objetoF = self.list_ctrl03

			if buscar:
				if self.enfocado == 2:
					__buscar = 'D'
				elif self.enfocado == 4:
					__buscar = 'A'
		else:
			return False

		if __path == '':
			#print('Por que esta el path vacio?')
			return False
		walking = os.walk(__path)
		listaDir = []
		listaFiles = []
		indice = 0
		objetoD.itemDataMap = {}
		objetoF.itemDataMap = {}

		objetoD.itemDataMap[0] = '...'

		for root, dirs, files in walking:
			#print('raiz', root)
			#print(dirs)
			indice = 1
			for directorio in dirs:
				listaDir.append(directorio)
				if __buscar == 'D':
					if directorio.lower().find(buscar.lower()) > -1:
						objetoD.itemDataMap[indice] = directorio
						indice +=1
				else:
					objetoD.itemDataMap[indice] = directorio
					indice +=1
			indice = 0
			for file in files:
				#print(file)
				#print(time.gmtime(os.path.getmtime(os.path.join(__path, file))))
				#print(type(time.gmtime(os.path.getmtime(os.path.join(__path, file)))))
				#horaO = time.strftime('%H:%M %d/%m/%Y',time.gmtime(os.path.getmtime(os.path.join(__path, file))))
				#horaO = time.strftime('%H:%M %d/%m/%Y',time.localtime(os.path.getmtime(os.path.join(__path, file))))
				horaO = time.strftime('%Y/%m/%d %H:%M',time.localtime(os.path.getmtime(os.path.join(__path, file))))
				listaFiles.append((file,horaO))
				#print(type(horaO),horaO)
				if __buscar == 'A':
					if file.lower().find(buscar.lower()) > -1:
						if self.__listaFiltrada[modo - 1] and not file.endswith('.py'):
							continue
						objetoF.itemDataMap[indice] = [file,horaO]
						indice += 1
					else:
						continue
				else:
					if self.__listaFiltrada[modo - 1] and not file.endswith('.py'):
						#print(file)
						continue
					objetoF.itemDataMap[indice] = [file,horaO]
					indice += 1
			break

		#print(objetoF.itemDataMap)
		#__color = (200,200,200)
		__color = (225,225,225)
		__color2 = (95, 198, 213)
		
		#objetoD.InsertItem(0, '...')
		#objetoD.SetItemData(0, 0)
		#objetoD.SetItemBackgroundColour(0, __color)
		__indexD = 0
		__indexF = 0
		try:
			for key,value in objetoD.itemDataMap.items():
				objetoD.InsertItem(__indexD,value)
				objetoD.SetItemData(__indexD, key)
				__indexD +=1
			"""
			for item in listaDir:
				objetoD.InsertItem(__indexD, item)
			
				if __indexD % 2:
					objetoD.SetItemBackgroundColour(__indexD, __color2)
				else:
					objetoD.SetItemBackgroundColour(__indexD, __color)
			"""

			#if self.resolucion[1] != 1080:
			#	objetoD.SetColumnWidth(0,200)
			objetoD.SetColumnWidth(1,wx.LIST_AUTOSIZE_USEHEADER)
			self.__pintarFilas(modo)

			#print(objetoF.itemDataMap)
			for key,value in objetoF.itemDataMap.items():
				objetoF.InsertItem(__indexF,value[0])
				objetoF.SetItem(__indexF,1, value[1])
				objetoF.SetItemData(__indexF, key)
				"""
				if __indexF % 2:
					objetoF.SetItemBackgroundColour(__indexF, __color)
				else:
					objetoF.SetItemBackgroundColour(__indexF, __color2)
				"""
				__indexF +=1

			"""
			for item in listaFiles:
				if item[0].find('.py') > -1 and item[0].find('.pyc') == -1:
					objetoF.InsertItem(__indexF, item[0])
					objetoF.SetItem(__indexF,1, item[1])
					if __indexF % 2:
						objetoF.SetItemBackgroundColour(__indexF, __color)
					else:
						objetoF.SetItemBackgroundColour(__indexF, __color2)
					__indexF += 1
			"""
			if self.resolucion[1] == 1080:
				objetoF.SetColumnWidth(0,wx.LIST_AUTOSIZE_USEHEADER)
			else:
				objetoF.SetColumnWidth(0,150)
			objetoF.SetColumnWidth(1,wx.LIST_AUTOSIZE_USEHEADER)
			self.__pintarFilas(modo + 2)
		except Exception as e:
			print(e)
			print(__indexF)

	def __refrescar(self):
		self.__refrescarLista(1)
		self.__refrescarLista(2)

	def __alternarListas(self, modo = 'DESACTIVAR'):
		self.__vaciarPaneles()
		
		for child in self.GetChildren():
			#print(child)
			child.Destroy()
		if modo == 'DESACTIVAR':
			self.__listaEditable = [False, False, False, False]
		elif modo == 'ACTIVAR':
			self.__listaEditable = [True, True, True, True]
		else:
			self.__listaEditable[modo - 1] = not self.__listaEditable[modo - 1]
		self.__iniciarObjetos()
		self.__parent.SizerPrincipal.Layout()
		self.__refrescar()
		#self.__parent.SetSize(self.__size)
		#self.__parent.Maximize(True)
		#self.__parent.Update()
		#self.__parent.Layout()
		#self.__parent.Fit()
		#self.__parent.Show()
		"""
		self.__parent.SizerPrincipal.Layout()
		self.__parent.Maximize(True)
		self.__parent.Maximize(False)
		self.__parent.Maximize(True)
		self.__parent.Show()
		self.__parent.Raise()
		self.__parent.Update()
		"""
		#modo = modo if modo in [1,2] else modo - 2

	def __filtrarLista(self, id):
		if id == 'todo':
			self.__listaFiltrada = [True, True]
		elif id == 'nada':
			self.__listaFiltrada = [False, False]
		else:
			self.__listaFiltrada[id - 3] = not self.__listaFiltrada[id - 3]
		self.__refrescar()

	def __pintarFilas(self, id):
		__color = (225,225,225)
		if id == 1:
			objeto = self.list_ctrl00
			__color2 = (247,148,91)
			__color2 = (178, 252, 255)
		elif id ==2:
			objeto = self.list_ctrl02
			__color2 = (247,148,91)
			__color2 = (178, 252, 255)
		elif id == 3:
			objeto = self.list_ctrl01
			__color2 = (134,188,236)
			__color2 = (94, 223, 255)
		elif id == 4:
			objeto = self.list_ctrl03
			__color2 = (134,188,236)
			__color2 = (94, 223, 255)
		#sel = objeto.GetSelection()
		#print(sel)
		#text = objeto.GetString(sel)
		#print(text)
		
		
		#azules
		#__color2 = (175,225,236)
		#__color2 = (134,188,236)
		#naranjas
		#__color2 = (247,148,91)
		
		count = objeto.GetItemCount()
		#print(count)
		for i in range(count):
			#item = objeto.GetItem(i,0)
			#print(item.GetText())
			if i > 0 and i % 2:
				objeto.SetItemBackgroundColour(i, __color2)
			else:
				objeto.SetItemBackgroundColour(i, __color)

	def __desactivarEdicion(self):
		self.__alternarListas('DESACTIVAR')
		try:
			self.__parent.SetStatusText("Copyright TOI")
		except Exception as e:
			print(e)

	def __activarEdicion(self):
		self.__alternarListas('ACTIVAR')
		try:
			self.__parent.SetStatusText("Copyright TOI - //MODO EDICION ACTIVADO//")
		except Exception as e:
			print(e)

	def __cambiarDirectorio(self, modo = 1,  bajar = False):
		if modo == 1:
			__path = self.path
		elif modo == 2:
			__path = self.path2
		if not bajar:
			ubicador = __path.split('\\')
			#print(ubicador)
			if len(ubicador) > 2:
				limpia = '\\' + ubicador[-1]
				__path = __path.replace(limpia, '')
			elif len(ubicador) == 2:
				__path = __path.replace(ubicador[-1], '')
		else:
			if __path[-1] != '\\':
				__path = __path + '\\' + bajar
			else:
				__path = __path + bajar

		if modo == 1:
			self.path = __path
		elif modo == 2:
			self.path2 = __path

	def __buscarPareja(self, modo, texto):
		__color = (225,225,225)
		__color2 = (94, 223, 255)
		__color3 =  (250, 83, 83)
		if modo == 1:
			objeto = self.list_ctrl02
		elif modo == 2:
			objeto = self.list_ctrl00
		elif modo == 3:
			objeto = self.list_ctrl03
		elif modo == 4:
			objeto = self.list_ctrl01
		count = objeto.GetItemCount()
		#print(objeto.GetTopItem())
		#print(objeto.GetCountPerPage())
		for i in range(count):
			item = objeto.GetItem(i,0)
			#print(item.GetText())
			#print(item.GetState())
			if item.GetState() != 0: # == 6
				#item.SetStateMask(0)
				#item.SetState(wx.LIST_STATE_SELECTED|wx.LIST_STATE_FOCUSED)
				objeto.Select(i, False)
				#objeto.Focus(i)
				#print(item.GetState())
			if item.GetText() == texto:
				objeto.SetItemBackgroundColour(i, __color3)
				objeto.EnsureVisible(i)
			elif i > 0 and i % 2:
				objeto.SetItemBackgroundColour(i, __color2)
			else:
				objeto.SetItemBackgroundColour(i, __color)

	def __copiarArchivo(self, modo, nombre):
		if not os.path.isdir(self.path) or not os.path.isdir(self.path2):
			print('Uno de los directorios no es valido para poder copiar')
			return False
		if self.path[-1] != '\\':
			__path = self.path + '\\'
		else:
			__path = self.path

		if self.path2[-1] != '\\':
			__path2 = self.path2 + '\\'
		else:
			__path2 = self.path2

		if modo == 3:
			__origenPath = __path + nombre
			__destinoPath = __path2 + nombre
			__actualiza = 2
		elif modo == 4:
			__origenPath = __path2 + nombre
			__destinoPath = __path  + nombre
			__actualiza = 1
		else:
			print('Modo %d para carpeta %s' % (modo, nombre))
			return False

		"""
		print('Estamos en modo %d' % modo)
		print('Habria que copiar')
		print('De %s' % __origenPath)
		print('A %s' % __destinoPath)
		"""
		try:
			shutil.copy2(__origenPath, __destinoPath)
		except Exception as e:
			print(e)

		self.__refrescarLista(__actualiza)

	def __borrarArchivo(self, nombre):
		#print(nombre)
		if os.path.isfile(nombre):
			print('%s es un archivo y lo voy a borrar' % nombre)
			os.remove(nombre)
			return True
		return False

	def __moverArchivo(self, modo, nombre):
		if not os.path.isdir(self.path) or not os.path.isdir(self.path2):
			print('Uno de los directorios no es valido para poder mover')
			return False
		print('mover archivo %s' % nombre)

	def __startLanzar(self, nombre):
		#print('start "" "%s"' % nombre)
		comando = 'start "" "%s"' % nombre
		hilo = Thread(target=os.system, args=(comando,))
		hilo.start()

	def __ejecutarPython(self, nombre, modo = ''):
		comando = 'python%s "%s"' % (modo, nombre)
		#print(comando)
		hilo = Thread(target=os.system, args=(comando,))
		hilo.start()
		#os.system(comando)

	def __renombrar(self, nombreO, nombreD):
		#print('Renombrar: %s a %s' % (nombreO, nombreD))
		if nombreO == nombreD:
			return False
		if os.path.exists(nombreO):
			os.rename(nombreO, nombreD)

	def __copiarDirectorio(self, modo, texto):
		if self.path == '' or self.path2 == '':
			return False
		if modo == 1:
			__origen = self.path
			__destino = self.path2
		else:
			__origen = self.path2
			__destino = self.path

		__root = texto
		__origen = __origen + '\\' + __root
		__destino = __destino + '\\' + __root
		print('origen: %s' % __origen)
		print('destino: %s' % __destino)
		print('carpeta: %s' % __root)
		if not os.path.exists(__destino):
			print('destino no existe, se crea')
			#os.mkdir(ruta_destino)
		else:
			print('destino existe')

		i = j = z = 0
		for root, dirs, files in os.walk(__origen):
			for directorio in dirs:
				ruta_destino = os.path.join(root.replace(__origen, __destino), directorio)
				if not os.path.exists(ruta_destino):
					#os.mkdir(ruta_destino)
					#print('Aqui creo carpeta')
					i += 1
				else:
					j += 1
					#print('Ruta destino existe: %s' % ruta_destino)

			for file in files:
				if file.endswith('.py'):
					
					__fileO = os.path.join(root, file)
					__fileD = os.path.join(root.replace(__origen,__destino),file)

					#print('Tocaria copiar %s en %s' % (__fileO, __fileD))
					z += 1
					#shutil.copy2(__fileO, __fileD))

		resultado = 'Se han copiado %d directorios de los cuales\n%d ya existian y %d se han creado.\nSe han copiado un total de %d archivos.' % (i+j, j, i, z)
		print(resultado)
		wx.MessageBox(resultado, 'Resultado copia', wx.OK|wx.ICON_INFORMATION)

	def __moverDirectorio(self):
		pass

	def __borrarDirectorio(self):
		pass

	def __emergente(self, opciones):
		self.popup_menu = wx.Menu()
		self.opcionesPopUp = {}
		for opcion in opciones:
			#__menu.Append(wx.NewId(), opcion)
			item = self.popup_menu.Append(-1, opcion)
			#print(item)
			self.opcionesPopUp[item] = opcion
			self.Bind(wx.EVT_MENU, self.OnPopUp, item)

		self.__accionPopUp = ''
		self.PopupMenu(self.popup_menu)
		self.popup_menu.Destroy()

	def refrescarLista(self, modo = 1):
		self.__refrescarLista(modo)

	def buscarLista(self, texto):
		if self.enfocado in [1,3]:
			modo = 1
		elif self.enfocado in [2,4]:
			modo = 2
		else:
			return False
		self.__refrescarLista(modo, texto)
	
	def emergente(self, opciones):
		self.__emergente(opciones)
		return False if self.__accionPopUp == '' else True

	def desactivarEdicion(self):
		self.__desactivarEdicion()

	def OnList(self,event):
		#print(event.GetItem())
		#print(event.m_itemIndex)
		select = event.GetText()
		__id = int(event.GetId() / 10)

		#print('select: %s' % select)
		#print('select2: %s' % select2)
		#print('Entro aqui aunque no proceda?')
		if select == '...':
			__bajar = False
		else:
			__bajar = select

		if __id in [1,2]:
			self.__cambiarDirectorio(modo = __id, bajar = __bajar)
			self.__refrescarLista(modo = __id)
		elif __id in [3,4]:
			if __id == 4:
				opciones =['confirma copiar']
				self.__emergente(opciones)
				if self.__accionPopUp == '':
					return False
			self.__copiarArchivo(__id, __bajar)

	def OnPressKey(self, event):
		try:
			keycode = event.GetKeyCode()
			#print(keycode)
			__id = int(event.GetId() / 10)
			#print(__id)
			texto = event.GetText()		
			#print(texto)
		except:
			print('return')
			return False
		
		if keycode == 127: # 127 -> SUPR; 27 -> ESC
			__mas = '\\'
			if __id == 3:
				__path = self.path
				opciones =['confirma borrar']
				self.__emergente(opciones)
				if self.__accionPopUp == '':
					return False
				if self.path[-1] == '\\':
					__mas = ''
			elif __id == 4:
				__path = self.path2
				if self.path2[-1] == '\\':
					__mas = ''
			else:
				return False
			self.__borrarArchivo(__path + __mas + texto)
			self.__refrescarLista(__id - 2)	
		elif keycode == 341: # F2
			#print(event.GetEventObject())
			#print(keycode)
			#print(__id)
			#print(texto)
			self.__alternarListas(__id)
						
	def OnMouseRight(self,event):
		try:
			__id = int(event.GetId() / 10)
			#print(__id)
			texto = event.GetText()		
			#print(texto)
			#print(event.GetPosition())
		except Exception as e:
			print(e)
			return False

		if __id in [1,2]:
			#opciones = ['copiar', 'mover', 'renombrar', 'borrar']
			opciones = ['copiar', 'mover', 'renombrar']
			__funciones = {'copiar':self.__copiarDirectorio, 'mover':self.__moverDirectorio, 'renombrar':self.__renombrar,'borrar':self.__borrarDirectorio, 'activar edicion':self.__alternarListas, 'desactivar edicion':self.__alternarListas}
		elif __id in [3,4]:
			opciones = ['copiar', 'mover', 'renombrar', 'borrar', 'lanzar', 'python', 'python3']
			if self.__listaFiltrada[__id - 3]:
				opciones.append('desfiltrar')
			else:
				opciones.append('filtrar')
			#opciones = ['copiar', 'mover', 'renombrar', 'lanzar']
			__funciones = {'copiar':self.__copiarArchivo, 'mover':self.__moverArchivo, 'renombrar':self.__renombrar,'borrar':self.__borrarArchivo, 'lanzar':self.__startLanzar, 'activar edicion':self.__alternarListas, 'desactivar edicion':self.__alternarListas, 'filtrar':self.__filtrarLista, 'desfiltrar':self.__filtrarLista, 'python':self.__ejecutarPython, 'python3':self.__ejecutarPython}
		else:
			return False

		if self.__listaEditable[__id - 1]:
			opciones.append('desactivar edicion')
		else:
			opciones.append('activar edicion')
			opciones.remove('renombrar')
		__mas = '\\' 
		if __id in [1,3]:
			if self.path[-1] == '\\':
				__mas = ''
			__ruta = self.path + __mas + texto
			__refresh = 1

		elif __id in [2,4]:
			if self.path2[-1] == '\\':
				__mas = ''
			__ruta = self.path2 + __mas + texto
			__refresh = 2

		self.__emergente(opciones)
		#print('Tengo que %s la carpeta %s' % (self.__accionPopUp, texto))
		if self.__accionPopUp == '':
			return False
		elif self.__accionPopUp == 'borrar' and __id in [1,3]:
			opciones = ['confirma borrar']
			self.__emergente(opciones)
			if self.__accionPopUp == '':
				return False
			self.__accionPopUp = 'borrar'
		elif self.__accionPopUp == 'copiar' and __id in [2,4]:
			opciones =['confirma copiar']
			self.__emergente(opciones)
			if self.__accionPopUp == '':
				return False
			self.__accionPopUp = 'copiar'

		if self.__accionPopUp in ['borrar', 'lanzar', 'python', 'python3']:
			if self.__accionPopUp == 'python3':
				__funciones[self.__accionPopUp](__ruta, '3')
			else:
				__funciones[self.__accionPopUp](__ruta)
			if self.__accionPopUp == 'borrar':
				self.__refrescarLista(__refresh)
		elif self.__accionPopUp in ['copiar', 'mover']:
				__funciones[self.__accionPopUp](__id, texto)
		elif self.__accionPopUp in ['activar edicion', 'desactivar edicion', 'filtrar', 'desfiltrar']:
			__funciones[self.__accionPopUp](__id)				

		self.__accionPopUp = ''

	def OnPopUp(self,event):
		try:
			__id = event.GetId()
			#print(__id)
			item = self.popup_menu.FindItemById(__id)
			self.__accionPopUp = self.opcionesPopUp[item]
		except Exception as e:
			print(e)
			return False
		
	def OnRightClick(self, event):
		#print(event.GetId())
		#print('Orc')
		opciones = ['refrescar', 'activar edicion', 'desactivar edicion']
		if not (self.__listaFiltrada[0] and self.__listaFiltrada[1]):
			opciones.append('filtrar')
		else:
			opciones.append('desfiltrar')
		self.__emergente(opciones)
		#print('Tengo que %s la carpeta %s' % (self.__accionPopUp, texto))
		if self.__accionPopUp == '':
			return False
		if self.__accionPopUp == 'refrescar':
			self.__refrescar()
		elif self.__accionPopUp == 'activar edicion':
			self.__activarEdicion()
		elif self.__accionPopUp == 'desactivar edicion':
			self.__desactivarEdicion()
		elif self.__accionPopUp == 'filtrar':
			self.__filtrarLista('todo')
			self.__refrescar()
		elif self.__accionPopUp == 'desfiltrar':
			self.__filtrarLista('nada')
			self.__refrescar()

	def OnUpdateItem(self, event):
		#event.GetEventObject()
		#__id directorios 1,2 archivos 3,4
		__id = int(event.GetId() / 10)
		#print(__id)
		__item = event.GetLabel()
		if __item == '':
			return False
		#print('Item: %s' % __item)
		__indice = event.GetIndex()
		#print('Num item: %d' % __indice)
		__columna = event.GetColumn()
		#print('Num columna: %d' % __columna)
		if __columna == 1:
			return False
		if __id == 1:
			__objeto = self.list_ctrl00
			__ruta =self.path
			modo = 1
		elif __id == 2:
			__objeto = self.list_ctrl02
			__ruta =self.path2
			modo = 2
		elif __id == 3:
			__objeto = self.list_ctrl01
			__ruta =self.path
			modo = 1
		elif __id == 4:
			__objeto = self.list_ctrl03
			__ruta =self.path2
			modo = 2

		__nombreOriginal = __ruta + '\\' + __objeto.GetItem(__indice, __columna).GetText()
		__nombreFinal = __ruta + '\\' + __item

		self.__renombrar(__nombreOriginal, __nombreFinal)
		#print(__objeto.GetItem(__indice, __columna).GetText())

	def OnColClick(self,event):
		#print('Col click')
		#print(event.GetId())
		__id = int(event.GetId() / 10)
		event.Skip()
		self.__pintarFilas(__id)

	def OnSelected(self, event):
		try:
			texto = event.GetText()
		except:
			texto = ''
		__id = int(event.GetId() / 10)
		#item = event.GetItem()
		#print(item.GetText())
		#print(item.GetState())
		#print(texto)
		#print(__id)
		if texto == '':
			self.__pintarFilas(1)
			self.__pintarFilas(2)
			self.__pintarFilas(3)
			self.__pintarFilas(4)
			return True
		elif texto == '...':
			return True

		if __id in [3,4]:
			self.__pintarFilas(1)
			self.__pintarFilas(2)
		elif __id in [1,2]:
			self.__pintarFilas(3)
			self.__pintarFilas(4)

		self.__pintarFilas(__id)
		self.__buscarPareja(__id, texto)

	def OnReleaseKey(self, event):
		keycode = event.GetKeyCode()
		print(keycode)
		__id = int(event.GetId() / 10)
		print(__id)
		
	def onFocus(self, event):
		#print('onfoco')
		self.enfocado = int(event.GetId() / 10)

	def __resolucion(self):
		# (1280, 1024)
		# (1920, 1080)
		user32 = windll.user32
		screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
		return screensize	

if __name__ == "__main__":
	ventana = wx.App()
	frame = wxCommander()
	#frame.Show()
	ventana.MainLoop()