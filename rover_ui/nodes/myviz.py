from PyQt5.QtCore import Qt
import roslib
import sys
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QSlider, QVBoxLayout, QWidget,QApplication
import rviz

class myviz(QWidget):
    def __init__(self):
        super(myviz,self).__init__()
        self.frame=rviz.VisualizationFrame()
        self.frame.setSplashPath("")
        self.frame.initialize()
        reader = rviz.YamlConfigReader()
        config = rviz.Config()
        reader.readFile( config, "config.myviz" )
        self.frame.load( config )
        self.setWindowTitle( config.mapGetChild( "Title" ).getValue() )
        self.manager = self.frame.getManager()
        self.grid_display = self.manager.getRootDisplayGroup().getDisplayAt( 0 )
        layout = QVBoxLayout()
        layout.addWidget( self.frame )

        self.setLayout( layout )

    

if __name__=="__main__":
    app=QApplication(sys.argv)
    win=myviz()
    win.show()
    sys.exit(app.exec_())