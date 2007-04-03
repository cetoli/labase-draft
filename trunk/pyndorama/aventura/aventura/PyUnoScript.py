import sys, os, tempfile, time
import uno, unohelper
from com.sun.star.connection import NoConnectException
from com.sun.star.beans import PropertyValue
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK
#-------- coloque este trecho
class UnoSection:
  def paragraph(self,value):
    doc.Text.insertString(cursor, value, False)
    doc.Text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
  def publish(self):
    cursor.ParaStyleName = "Heading 2"
    self.paragraph(self.title)
    self.paragraph(self.text)
class UnoTextValley(UnoSection):
  title="The Crow Flies to the Valley"
  text="The valley is still green, despites the long lasting draught"
class UnoTextRiver(UnoSection):
  title="The Crow Flies to the River"
  text="To his dismay, he can see only a dry river bed"
class UnoDocumentCrowAndPitcher:
  def publish(self):
    UnoTextValley().publish()
    UnoTextRiver().publish()
#--- fim do trecho -------------------    
# get the uno component context from the PyUNO runtime
localContext = uno.getComponentContext()
# create the UnoUrlResolver
resolver = localContext.ServiceManager.createInstanceWithContext(
				"com.sun.star.bridge.UnoUrlResolver", localContext )
# connect to the running office
ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
smgr = ctx.ServiceManager

# get the central desktop object
desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)

# access the current writer document
model = desktop.getCurrentComponent()
doc = desktop.loadComponentFromURL("private:factory/swriter",'_blank',0,())
doc.Text.String
cursor = doc.Text.createTextCursor()
UnoDocumentCrowAndPitcher().publish()
cursor = doc.Text.createTextCursorByRange(doc.Text.Start)
anIndex =doc.createInstance("com.sun.star.text.ContentIndex")
anIndex.supportsService("com.sun.star.text.ContentIndex")
anIndex.CreateFromOutline = True
anIndex.CreateFromLevelParagraphStyles = True
anIndex.CreateFromChapter = False
anIndex.IsProtected=False
doc.Text.insertTextContent(cursor, anIndex, False)
anIndex.update()
anIndex.HeaderSection.Anchor.String = "The Crow & the Pitcher"



