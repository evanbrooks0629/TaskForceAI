from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import json

class ClickableFrame(QFrame):
    # acts as a button
    def __init__(self, currentAgent, widget):
        super().__init__()

        self.widget = widget # Keeps track of associated Agents class

        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # import any information needed from the agent for editing
        self.name = currentAgent['name']
        self.description = currentAgent['description']
        self.system_message = currentAgent['system_message']
        self.skills = currentAgent['skills']

        self.clicked = False #variable to keep tracked of click

    def mousePressEvent(self, event):
        print(self.name ,"Frame Clicked!")
        self.widget.resetBorders(self)
        self.clicked = not self.clicked
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.clicked:
            painter = QPainter(self)
            color = QColor(117, 219, 233)  # From Figma
            pen = QPen(color, 3, Qt.PenStyle.SolidLine)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)  # For rounded corners
            painter.setPen(pen)
            painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 10, 10)  

class AddAgentButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clicked = False
        self.setStyleSheet("""
            background-color: transparent;
            border: 2px solid #75DBE9;
            height: 50;
            border-radius: 10;
            color: #75DBE9;
        """)
        self.setText("Add Agent")
    
    def mousePressEvent(self, event):
        print("Adding Agent Clicked")


class AgentsFrame(QFrame):
    def __init__(self):
        super().__init__()

        # Keep track of all agent boxes
        self.allBoxes = []

        # Set tab style
        # frame = QFrame()
        self.setStyleSheet("background-color: #464545; border-radius: 20;")
        mainhbox = QHBoxLayout()

        # Fixed frame to embed the scroll section in
        viewFrame = QFrame()
        viewFrame.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        viewVBox = QVBoxLayout()

        # Scroll section
        agents = self.loadAgents()
        agentScroll = QScrollArea()
        agentScroll.setWidgetResizable(True)
        agentScroll.setWidget(agents)
        agentScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        agentScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # Embed scroll into view agents section
        viewVBox.addWidget(agentScroll)
        viewFrame.setLayout(viewVBox)
       
        agentsTasksFrame = QFrame()
        agentsTasksFrame.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        agentsTasksVBox = QVBoxLayout()
        agentsTasksFrame.setLayout(agentsTasksVBox)

        mainhbox.addWidget(viewFrame)
        mainhbox.addWidget(agentsTasksFrame)

        mainhbox.setStretchFactor(viewFrame, 1) #equally sized left and right panels
        mainhbox.setStretchFactor(agentsTasksFrame, 1)
        self.setLayout(mainhbox)
        

    def agentBox(self, list_of_agent_objects):
        bold = QFont()
        bold.setBold(True)

        agentsFrame = QFrame()
        agentsLayout = QGridLayout()
        agentsLabel = QLabel("Agents")
        agentsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        agentsLabel.setFont(bold)
        agentsFrame.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        agentsLayout.addWidget(agentsLabel, 0, 0, 1, 3)  # Span label across 3 columns

        addButton = AddAgentButton()
        # addButton.setFixedSize(80, 40)
        agentsLayout.addWidget(addButton, 0, 2, 1, 1)

        row, col = 1, 0
        for currentAgent in list_of_agent_objects:
            obj = currentAgent
            #print(obj)
            agentBox = ClickableFrame(obj, self)
            # agentBox.stretch
            agentBox.setFixedHeight(200)
            # agentBox.setS
            agentBox.setStyleSheet("""
                background-color: #464545;
                border-radius: 10;
            """)
            agentVBox = QVBoxLayout()
            name = obj['name']
            description = obj['description']
            system_message = obj["system_message"]
            skills = obj["skills"]
            nameLabel = QLabel(name)
            nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            nameLabel.setFont(bold)
            nameLabel.setFixedHeight(25)
            descriptionLabel = QLabel(description)
            descriptionLabel.setWordWrap(True)
            # descriptionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # systemMessageLabel = QLabel(system_message)
            # systemMessageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            agentVBox.addWidget(nameLabel)
            nameLine = QLabel()
            nameLine.setStyleSheet("""
                background-color: #5E5E5E;
                border-radius: 0;
            """)
            nameLine.setFixedHeight(2)
            agentVBox.addWidget(nameLine)
            descriptionLine = QLabel()
            descriptionLine.setStyleSheet("""
                background-color: #5E5E5E;
                border-radius: 0;
            """)
            descriptionLine.setFixedHeight(2)
            agentVBox.addWidget(descriptionLabel)
            agentVBox.addWidget(descriptionLine)
            # agentVBox.addWidget(systemMessageLabel)

            skillsText = QLabel("Functions:")
            agentVBox.addWidget(skillsText)


            for i in range(len(skills)):
                skillsLabel = QLabel(skills[i])
                skillsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                skillsLabel.setStyleSheet("""
                    border: 1px solid white;
                    padding-left: 2;
                    padding-right: 2;
                    border-radius: 5;
                    font-size: 24;
                """)
                skillsLabel.setFixedHeight(25)
                agentVBox.addWidget(skillsLabel)

            agentBox.setLayout(agentVBox)
            self.allBoxes.append(agentBox)
            agentsLayout.addWidget(agentBox, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

        agentsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        agentsFrame.setLayout(agentsLayout)
        return agentsFrame

    def resetBorders(self, clicked_frame):
        # Reset borders of all clickable frames except the clicked frame
        for current in self.allBoxes:
            if current != clicked_frame:
                current.clicked = False
                current.update()

    def loadAgents(self):
        file = open('./data/agents.json')
        data = json.load(file)
        agents = self.agentBox(data["agents"])
        return agents
        # loop through agents and display accordingly
### TODO:
    # [ ] Rename