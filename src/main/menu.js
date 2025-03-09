// 1.导入 electron 中的 Menu
const { Menu, BrowserWindow } = require('electron')

// 2.创建菜单模板,数组里的每一个对象都是一个菜单
const template = [
  
]

// 3.从模板中创建菜单
const myMenu = Menu.buildFromTemplate(template)

// 4.设置为应用程序菜单
Menu.setApplicationMenu(myMenu)
