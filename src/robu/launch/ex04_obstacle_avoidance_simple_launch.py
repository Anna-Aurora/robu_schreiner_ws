import os #betriebssystemmethoden drinnen

#gibt den Installationspfad eines Paketes zurück
from ament_index_python.packages import get_package_share_directory #wichtig für den Test!!!!!! fragt er

from launch import LaunchDescription
from launch_ros.actions import Node
import launch                #es wird alles importiert
from launch.actions import(
    SetEnvironmentVariable,
    IncludeLaunchDescription,
    DeclareLaunchArgument,
    
)
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition

#diese Datei lässt sich über das Kommand
#ros2 launch robu ex_04_ocstacle_avoidance_simple.launch.py
#starten
def generate_launch_description():
    #Umgebungsvariablen anlegen
    envar_id = SetEnvironmentVariable(name='ROS_DOMAIN_ID', value='17')
    envar_model = SetEnvironmentVariable(name='TURTLEBOT2_MODEL', value='burger')
    envar_lds_model = SetEnvironmentVariable(name='LDS_MODEL', value='LDS-02')

    use_gazebo = LaunchConfiguration('use_gazebo', default = 'True')
    larg_use_gazebo = DeclareLaunchArgument('use_gazebo', 
                                            default_value = 'True',
                                            description = 'Wether to start Gazebo')

#Variablenname                        Name später   Standartwert, wenn der Benutzer nichts angibt


    node_oas = Node(                   #startet das Programm robu &  den Ordner oas
        package='robu',             #Order in dem unser Programm ist/ Paketname
        executable='oas',           #festgelegt im setup.py
        name='Hinderniserkennung')


    node_remotectrl = Node(
            package='robu',
            executable='remotectrl',
            name='Fernbedienung',
            remappings = [('/cmd_vel', '/cmd_vel_raw')],             
            output='screen',
            #emulate_tty=True,
            prefix = 'gnome-terminal --' #öffnet ein neues Fenster für die Fernbedinung
   
     )
    
    ldes_gazebo = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('turtlebot3_gazebo'),
                                'launch', 'turtlebot3_dqn_stage1.launch.py')
            ),
            condition = IfCondition(use_gazebo) 
        )   
    ld = LaunchDescription()
    ld.add_action(envar_id)
    ld.add_action(envar_model)
    ld.add_action(envar_lds_model)
    ld.add_action(larg_use_gazebo)    
    ld.add_action(node_oas)
    ld.add_action(node_remotectrl)
    ld.add_action(ldes_gazebo)


    return ld
#wahlweise starten über launch argumente 




    # return LaunchDescription([ #in den Klammern sind alle Programme, die wir starten wollen; Alle Aktionen di er durchführen soll
    #     launch.actions.SetEnvironmentVariable(name='ROS_DOMAIN_ID', value='17'),
    #     launch.actions.SetEnvironmentVariable(name='TURTLEBOT2_MODEL', value='burger'), #Modell vom Roboter festlegen
    #     launch.actions.SetEnvironmentVariable(name='LDS_MODEL', value='LDS-02'), #Modell vom Lidar festlegen
    #     Node(                           #startet das Programm robu &  den Ordner oas
    #         package='robu',             #Order in dem unser Programm ist/ Paketname
    #         executable='oas',           #festgelegt im setup.py
    #         name='Hinderniserkennung'   #ros2 node list 
    #     ),
    #     Node(
    #         package='robu',
    #         executable='remotectrl',
    #         name='Fernbedienung',
    #         remappings = [('/cmd_vel', '/cmd_vel_raw')],  #cmd_vel wird umgenannt zu cmd_vel_raw
    #         #Hinderniserkennung als auch Ferbedingung wollen den Roboter gleichzeitig steuern (cmd_vel)
    #         #-> Remapping: DIe Fernbedingung sendet cmd_vel als cmd_vel_raw an die Hinderniserkenung
    #         #und die Hinderniserkennung entscheidet, ob die Daten an den Roboter gesendet werden
            
    #         output='screen',
    #        #emulate_tty=True,
    #        prefix = 'gnome-terminal --' #öffnet ein neues Fenster für die Fernbedinung

    #     ), 
    #     #importiert eine fremde launch-Date: startet Gazebo mit der Welt dqn_stage1
    #     IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource(
                    
    #                 os.path.join(get_package_share_directory('turtlebot3_gazebo'),
    #                              'launch', 'turtlebot3_dqn_stage1.launch.py')
    #             )
    #         )    


    # ])