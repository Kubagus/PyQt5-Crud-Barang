from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication

import sqlite3
import sys
import os 
os.system('python Connection.py')

# conn = sqlite3.connect("D:\Materi & Tugas Kuliah\Semester 3\PBO\SqLite\dbToko.db")
# curr = conn.cursor()

class MainWindow(QDialog):
    isEdit = False
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('frmBarang.ui', self)
        self.loadData()
        self.EventHandler()
        
    def EventHandler(self):
        self.btnSimpan.clicked.connect(self.SimpanData)
        self.btnEdit.clicked.connect(self.editData)
        self.btnDelete.clicked.connect(self.deleteData)
        self.btnCari.clicked.connect(self.cariData)
        self.tblwgBarang.clicked.connect(self.getItem)
        self.ActiveText(False)
        
    def SimpanData(self):
        conn = sqlite3.connect("dbToko.db")
        curr = conn.cursor()
        cb = self.btnSimpan.text()
        print(cb)
        if cb == 'Baru':
            self.ActiveText(True)
            self.clearForm()
            self.btnSimpan.setText('Simpan')
            self.btnEdit.setText('Batal')
            
        elif cb == 'Simpan':
            if self.isEdit == False:
                self.btnSimpan.setText('Baru')    
                kodeBarang = self.txtKodeBarang.text()
                namaBarang = self.txtNamaBarang.text()
                harga = self.txtHarga.text()
                stok = self.txtStok.text()
                
                query = "INSERT or IGNORE INTO tb_barang (kode_barang, nama_barang, harga, stok) VALUES (?, ?, ?, ?)"
                curr.execute(query,(kodeBarang,namaBarang,harga,stok))
                conn.commit()
                print("Simpan Berhasil")
               
            elif self.isEdit == True:
                kodeBarang = self.txtKodeBarang.text()
                namaBarang = self.txtNamaBarang.text()
                harga = self.txtHarga.text()
                stok = self.txtStok.text()               
                query = "UPDATE tb_barang SET nama_barang = ?, harga = ?, stok = ? WHERE kode_barang = ?"
                curr.execute(query,(namaBarang,harga,stok,kodeBarang))
                conn.commit()
                print("Edit Berhasil")
            curr.close()
            conn.close()
            self.loadData()
            self.ActiveText(False)
            self.clearForm()
            self.btnSimpan.setText('Baru')
            self.btnEdit.setText('Edit')
        
    def editData(self):
            if self.btnEdit.text() == 'Edit':
                self.btnEdit.setText('Batal')
                self.btnSimpan.setText('Simpan')
                self.ActiveText(True)
                self.isEdit = True
                
            elif self.btnEdit.text() == 'Batal':
                self.btnEdit.setText('Edit')
                self.btnSimpan.setText('Baru')
                self.ActiveText(False)
                self.clearForm()
        
    def deleteData(self):
        conn = sqlite3.connect("dbToko.db")
        curr = conn.cursor()
        query = "DELETE FROM tb_barang WHERE kode_barang = ?"
        kodeBarang = self.txtKodeBarang.text()
        curr.execute(query,(kodeBarang,))
        conn.commit()
        print("Hapus Berhasil")
        curr.close()
        conn.close()
        self.loadData()
        self.clearForm()
        
        
    def getItem(self):
        row = self.tblwgBarang.currentRow()
        kodeBarang = self.tblwgBarang.item(row, 0).text()
        namaBarang = self.tblwgBarang.item(row, 1).text()
        harga = self.tblwgBarang.item(row, 2).text()
        stok = self.tblwgBarang.item(row, 3).text()
        
        self.txtKodeBarang.setText(kodeBarang)
        self.txtNamaBarang.setText(namaBarang)
        self.txtHarga.setText(harga)
        self.txtStok.setText(stok)
        
        
    def clearForm(self):
        self.txtKodeBarang.setFocus()
        self.txtKodeBarang.setText("")
        self.txtNamaBarang.setText("")
        self.txtHarga.setText("0")
        self.txtStok.setText("0")
        return
    
    def ActiveText(self, bool):
        self.txtKodeBarang.setEnabled(bool)
        self.txtNamaBarang.setEnabled(bool)
        self.txtHarga.setEnabled(bool)
        self.txtStok.setEnabled(bool)
        self.tblwgBarang.setEnabled(bool)
        return
        
    def loadData(self):
        conn = sqlite3.connect("dbToko.db")
        curr = conn.cursor()
        
        query = f"SELECT * FROM tb_barang WHERE nama_barang LIKE '%{ self.txtCari.text()}%' ORDER BY kode_barang ASC"
        curr.execute(query)
        result = curr.fetchall()
        conn.commit()
        self.tblwgBarang.setRowCount(len(result))
        tableRow = 0

        for row in result:
            self.tblwgBarang.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tblwgBarang.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.tblwgBarang.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.tblwgBarang.setItem(tableRow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            tableRow +=1
        curr.close()
        conn.close()

    def cariData(self):
        self.loadData()
        
        
# Main
app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(600)
widget.setFixedWidth(650)
widget.show()

try:
    sys.exit(app.exec_())
    
except:
    print('Existing')

