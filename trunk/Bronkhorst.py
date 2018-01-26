#!/usr/bin/env python
# -*- coding:utf-8 -*-


# ############################################################################
#  license :
# ============================================================================
#
#  File :        Bronkhorst.py
#
#  Project :     
#
# This file is part of Tango device class.
# 
# Tango is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Tango is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Tango.  If not, see <http://www.gnu.org/licenses/>.
# 
#
#  $Author :      maxim.stassevich$
#
#  $Revision :    $
#
#  $Date :        $
#
#  $HeadUrl :     $
# ============================================================================
#            This file is generated by POGO
#     (Program Obviously used to Generate tango Object)
# ############################################################################

__all__ = ["Bronkhorst", "BronkhorstClass", "main"]

__docformat__ = 'restructuredtext'

import PyTango
import sys
# Add additional import
#----- PROTECTED REGION ID(Bronkhorst.additionnal_import) ENABLED START -----#
import serial
import serial.tools.list_ports
import threading
import time
from scipy import interpolate

class read_Bronkhorst_Thread(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        print "Bronkhorst thread: Starting thread"
        self.port = port
        self.running = True
        self.fault = False
        self.commandAllowed = False
        self.command = ""
                
        self.flow = 0.00
        self.setpoint = 0
        self.set_setpoint = 0
                
        self.ser = serial.Serial(              
               port = self.port,
               baudrate = 38400,
               parity = serial.PARITY_NONE,
               stopbits = serial.STOPBITS_ONE,
               bytesize = serial.EIGHTBITS,
               timeout = 1
               )
        
    def run(self):
        print "Bronkhorst thread: started"
        while self.running:
            try:
                if self.commandAllowed:
                    self.ser.write(self.command)
                    reply = self.ser.readline()
                    self.commandAllowed = False
                    self.command = ""
                self.ser.write(":06800401210120\r\n")                 
                data = self.ser.readline()
                data = data[11:15]
                data = int(data, 16)
                f = interpolate.interp1d([0,32000],[0,25])
                self.flow = f(data)
                #print self.flow

                self.ser.write(":06800401210121\r\n")                 
                data = self.ser.readline()
                data = data[11:15]
                data = int(data, 16)
                f = interpolate.interp1d([0,32000],[0,25])
                self.setpoint = f(data)
                
                self.fault = False
            except:
                self.fault = True
                #time.sleep(0.5)
        self.ser.close()
        print "Bronkhorst thread: died"
        
    def stop(self):
        print "Bronkhorst thread: Stopping thread"
        self.running = False
        
    def get_data(self):
        return self.fault, self.flow, self.setpoint, self.set_setpoint
    
    def send_command(self, command):
        self.command = command
        self.commandAllowed = True



#----- PROTECTED REGION END -----#	//	Bronkhorst.additionnal_import

# Device States Description
# ON : 
# OFF : 
# DISABLE : 


class Bronkhorst (PyTango.Device_4Impl):
    """Class for control Bronkhorst"""
    
    # -------- Add you global variables here --------------------------
    #----- PROTECTED REGION ID(Bronkhorst.global_variables) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	Bronkhorst.global_variables

    def __init__(self, cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        self.debug_stream("In __init__()")
        Bronkhorst.init_device(self)
        #----- PROTECTED REGION ID(Bronkhorst.__init__) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Bronkhorst.__init__
        
    def delete_device(self):
        self.debug_stream("In delete_device()")
        #----- PROTECTED REGION ID(Bronkhorst.delete_device) ENABLED START -----#
        self.get_thread.stop()
        if self.get_state() != PyTango.DevState.OFF:
            self.set_state(PyTango.DevState.OFF)
            self.set_status("Device is in OFF state")
        #----- PROTECTED REGION END -----#	//	Bronkhorst.delete_device

    def init_device(self):
        self.debug_stream("In init_device()")
        self.get_device_properties(self.get_device_class())
        self.attr_Flow_read = 0.0
        self.attr_Setpoint_read = 0.0
        #----- PROTECTED REGION ID(Bronkhorst.init_device) ENABLED START -----#
        self.On()
        #----- PROTECTED REGION END -----#	//	Bronkhorst.init_device

    def always_executed_hook(self):
        self.debug_stream("In always_excuted_hook()")
        #----- PROTECTED REGION ID(Bronkhorst.always_executed_hook) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Bronkhorst.always_executed_hook

    # -------------------------------------------------------------------------
    #    Bronkhorst read/write attribute methods
    # -------------------------------------------------------------------------
    
    def read_Flow(self, attr):
        self.debug_stream("In read_Flow()")
        #----- PROTECTED REGION ID(Bronkhorst.Flow_read) ENABLED START -----#
        attr.set_value(self.attr_Flow_read)
        
        #----- PROTECTED REGION END -----#	//	Bronkhorst.Flow_read
        
    def is_Flow_allowed(self, attr):
        self.debug_stream("In is_Flow_allowed()")
        if attr==PyTango.AttReqType.READ_REQ:
            state_ok = not(self.get_state() in [PyTango.DevState.OFF,
                PyTango.DevState.DISABLE])
        else:
            state_ok = not(self.get_state() in [])
        #----- PROTECTED REGION ID(Bronkhorst.is_Flow_allowed) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Bronkhorst.is_Flow_allowed
        return state_ok
        
    def read_Setpoint(self, attr):
        self.debug_stream("In read_Setpoint()")
        #----- PROTECTED REGION ID(Bronkhorst.Setpoint_read) ENABLED START -----#
        attr.set_value(self.attr_Setpoint_read)
        
        #----- PROTECTED REGION END -----#	//	Bronkhorst.Setpoint_read
        
    def is_Setpoint_allowed(self, attr):
        self.debug_stream("In is_Setpoint_allowed()")
        if attr==PyTango.AttReqType.READ_REQ:
            state_ok = not(self.get_state() in [PyTango.DevState.OFF,
                PyTango.DevState.DISABLE])
        else:
            state_ok = not(self.get_state() in [])
        #----- PROTECTED REGION ID(Bronkhorst.is_Setpoint_allowed) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Bronkhorst.is_Setpoint_allowed
        return state_ok
        
    def write_Set_setpoint(self, attr):
        self.debug_stream("In write_Set_setpoint()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Bronkhorst.Set_setpoint_write) ENABLED START -----#
        #value = "%.2f"%data
        f = interpolate.interp1d([0,25],[0,32000])
        newvalue = int(f(data))
        setpoint = str(hex(newvalue))
        setpoint = setpoint[2:]
        setpoint = str(setpoint)
        if len(setpoint) == 3:
            setpoint = "0" + setpoint
        elif len(setpoint) == 2:
            setpoint = "00" + setpoint
        elif len(setpoint) == 1:
            setpoint = "000" + setpoint
        command = ":0680010121" + setpoint + "\r\n"
        self.get_thread.send_command(command)
        #----- PROTECTED REGION END -----#	//	Bronkhorst.Set_setpoint_write
        
    def is_Set_setpoint_allowed(self, attr):
        self.debug_stream("In is_Set_setpoint_allowed()")
        if attr==PyTango.AttReqType.READ_REQ:
            state_ok = not(self.get_state() in [PyTango.DevState.OFF,
                PyTango.DevState.DISABLE])
        else:
            state_ok = not(self.get_state() in [PyTango.DevState.OFF,
                PyTango.DevState.DISABLE])
        #----- PROTECTED REGION ID(Bronkhorst.is_Set_setpoint_allowed) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Bronkhorst.is_Set_setpoint_allowed
        return state_ok
        
    def read_attr_hardware(self, data):
        self.debug_stream("In read_attr_hardware()")
        #----- PROTECTED REGION ID(Bronkhorst.read_attr_hardware) ENABLED START -----#
        if self.get_state() != PyTango.DevState.OFF:
            fault, flow, setpoint, set_setpoint = self.get_thread.get_data()
            if fault == True:
                if self.get_state() != PyTango.DevState.DISABLE:
                    self.set_state(PyTango.DevState.DISABLE)
                    self.set_status("Device is in Disable state")
            else:
                if self.get_state() != PyTango.DevState.ON:
                    self.set_state(PyTango.DevState.ON)
                    self.set_status("Device is in ON state")
                self.attr_Flow_read = flow
                self.attr_Setpoint_read = setpoint
                self.attr_Set_setpoint_read = set_setpoint
        #----- PROTECTED REGION END -----#	//	Bronkhorst.read_attr_hardware


    # -------------------------------------------------------------------------
    #    Bronkhorst command methods
    # -------------------------------------------------------------------------
    
    def On(self):
        """ 
        """
        self.debug_stream("In On()")
        #----- PROTECTED REGION ID(Bronkhorst.On) ENABLED START -----#
        if self.get_state() != PyTango.DevState.ON:
            self.set_state(PyTango.DevState.ON)
            self.set_status("Device is in ON state")
        self.get_thread = read_Bronkhorst_Thread(self.port)
        self.get_thread.start()
        #----- PROTECTED REGION END -----#	//	Bronkhorst.On
        
    def is_On_allowed(self):
        self.debug_stream("In is_On_allowed()")
        state_ok = not(self.get_state() in [PyTango.DevState.ON,
            PyTango.DevState.DISABLE])
        #----- PROTECTED REGION ID(Bronkhorst.is_On_allowed) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Bronkhorst.is_On_allowed
        return state_ok
        
    def Stop(self):
        """ 
        """
        self.debug_stream("In Stop()")
        #----- PROTECTED REGION ID(Bronkhorst.Stop) ENABLED START -----#
        self.get_thread.stop()
        if self.get_state() != PyTango.DevState.OFF:
            self.set_state(PyTango.DevState.OFF)
            self.set_status("Device is in OFF state")
        #----- PROTECTED REGION END -----#	//	Bronkhorst.Stop
        
    def is_Stop_allowed(self):
        self.debug_stream("In is_Stop_allowed()")
        state_ok = not(self.get_state() in [PyTango.DevState.OFF])
        #----- PROTECTED REGION ID(Bronkhorst.is_Stop_allowed) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Bronkhorst.is_Stop_allowed
        return state_ok
        

    #----- PROTECTED REGION ID(Bronkhorst.programmer_methods) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	Bronkhorst.programmer_methods

class BronkhorstClass(PyTango.DeviceClass):
    # -------- Add you global class variables here --------------------------
    #----- PROTECTED REGION ID(Bronkhorst.global_class_variables) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	Bronkhorst.global_class_variables


    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        'port':
            [PyTango.DevString, 
             '',
            ["/dev/ttyUSB0"] ],
        }


    #    Command definitions
    cmd_list = {
        'On':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        'Stop':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        }


    #    Attribute definitions
    attr_list = {
        'Flow':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ],
            {
                'label': "Flow",
                'unit': "l/min",
            } ],
        'Setpoint':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ],
            {
                'label': "Setpoint",
                'unit': "l/min",
            } ],
        'Set_setpoint':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.WRITE],
            {
                'label': "Set_setpoint",
                'unit': "l/min",
            } ],
        }


def main():
    try:
        py = PyTango.Util(sys.argv)
        py.add_class(BronkhorstClass, Bronkhorst, 'Bronkhorst')
        #----- PROTECTED REGION ID(Bronkhorst.add_classes) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Bronkhorst.add_classes

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed as e:
        print ('-------> Received a DevFailed exception:', e)
    except Exception as e:
        print ('-------> An unforeseen exception occured....', e)

if __name__ == '__main__':
    main()
