#!/usr/bin/env python


# """
# GLOBALS START
# """
TEMPCHECK_INTERVAL = 2
RINSE_DURATION = 1
CAUSTIC_DURATION = 1
ACID_DURATION = 1
SANITIZER_DURATION = 1
PURGE_DURATION = 1
PRESSURIZE_DURATION = 1
NUMBER_OF_STEPS = 14
# """
# GLOBALS END
# """


import sys
import time
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GObject
except:
    sys.exit(1)

class GuiGTK:
    """This is the main GTK application"""

    def __init__(self):
        self.gladefile = "./gui.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)

        self.handlers = {
                    "on_btnFullCycle_clicked": self.btnFullCycle_clicked,
                    "on_btnAbort_clicked": self.btnAbort_clicked,
                    "on_btnRinse_toggled": self.btnRinse_clicked,
                    "on_btnCaustic_toggled": self.btnCaustic_clicked,
                    "on_btnAcid_toggled": self.btnAcid_clicked,
                    "on_btnSanitizer_toggled": self.btnSanitizer_clicked,
                    "on_btnO2Purge_toggled": self.btnO2Purge_clicked,
                    "on_btnCO2Pressurize_toggled": self.btnCO2Pressurize_clicked,
                    "on_btnCO2Purge_toggled": self.btnCO2Purge_clicked,
                    "on_btnShutdown_toggled": self.btnShutdown_clicked,

                    "on_switchWaterIn_state_set": self.switchWaterIn_state_set,
                    "on_switchCausticIn_state_set": self.switchCausticIn_state_set,
                    "on_switchAcidIn_state_set": self.switchAcidIn_state_set,
                    "on_switchSanitizerIn_state_set": self.switchSanitizerIn_state_set,
                    "on_switchPumpIn_state_set": self.switchPumpIn_state_set,
                    "on_switchPumpPower_state_set": self.switchPumpPower_state_set,
                    "on_switchPumpOut_state_set": self.switchPumpOut_state_set,
                    "on_switchAir_state_set": self.switchAir_state_set,
                    "on_switchCO2_state_set": self.switchCO2_state_set,
                    "on_switchSanitizerOut_state_set": self.switchSanitizerOut_state_set,
                    "on_switchAcidOut_state_set": self.switchAcidOut_state_set,
                    "on_switchCausticOut_state_set": self.switchCausticOut_state_set,
                    "on_switchWaterOut_state_set": self.switchWaterOut_state_set,
                    "on_switchCausticHeater_state_set": self.switchCausticHeater_state_set,
                    "on_switchAcidHeater_state_set": self.switchAcidHeater_state_set
        }
        self.builder.connect_signals(self.handlers)

        self.window = self.builder.get_object("mainWindow")
        self.window.resize(800,480)
        self.window.show_all()

        self.btnFullCycle = self.builder.get_object("btnFullCycle")
        self.btnShutdown = self.builder.get_object("btnShutdown")
        self.btnRinse = self.builder.get_object("btnRinse")
        self.btnCaustic = self.builder.get_object("btnCaustic")
        self.btnAcid = self.builder.get_object("btnAcid")
        self.btnSanitizer = self.builder.get_object("btnSanitizer")
        self.btnO2Purge = self.builder.get_object("btnO2Purge")
        self.btnCO2Purge = self.builder.get_object("btnCO2Purge")
        self.btnCO2Pressurize = self.builder.get_object("btnCO2Pressurize")

        self.switchWaterIn = self.builder.get_object("switchWaterIn")
        self.switchCausticIn = self.builder.get_object("switchCausticIn")
        self.switchAcidIn = self.builder.get_object("switchAcidIn")
        self.switchSanitizerIn = self.builder.get_object("switchSanitizerIn")
        self.switchPumpIn = self.builder.get_object("switchPumpIn")
        self.switchPumpPower = self.builder.get_object("switchPumpPower")
        self.switchPumpOut = self.builder.get_object("switchPumpOut")
        self.switchAir = self.builder.get_object("switchAir")
        self.switchCO2 = self.builder.get_object("switchCO2")
        self.switchSanitizerOut = self.builder.get_object("switchSanitizerOut")
        self.switchAcidOut = self.builder.get_object("switchAcidOut")
        self.switchCausticOut = self.builder.get_object("switchCausticOut")
        self.switchWaterOut = self.builder.get_object("switchWaterOut")
        self.switchCausticHeater = self.builder.get_object("switchCausticHeater")
        self.switchAcidHeater = self.builder.get_object("switchAcidHeater")

        self.lblStatus = self.builder.get_object("lblStatus")
        self.lblCausticTemp = self.builder.get_object("lblCausticTemp")
        self.lblAcidTemp = self.builder.get_object("lblAcidTemp")
        self.levelBar = self.builder.get_object("levelBar")
        self.levelBar2 = self.builder.get_object("levelBar2")

        GObject.timeout_add_seconds(TEMPCHECK_INTERVAL, self.temperatureCheck)

        self.stopTimer = False
        self.fullCycleProgess = 1
        self.step = {1:self.btnO2Purge, 2:self.btnRinse, 3:self.btnO2Purge,
                     4:self.btnCaustic, 5:self.btnO2Purge, 6:self.btnRinse,
                     7:self.btnO2Purge, 8:self.btnAcid, 9:self.btnO2Purge,
                     10:self.btnRinse, 11:self.btnO2Purge, 12:self.btnSanitizer,
                     13:self.btnCO2Purge, 14:self.btnCO2Pressurize}

        self.readyToMoveOn = True
        self.fullCycleRunning = False

        self.DELETEME = 0

# """
# HELPER FUNCTIONS START
# """
    def temperatureCheck(self):
        self.switchAcidHeater.activate()
        self.switchCausticHeater.activate()

        self.lblAcidTemp.set_label("Acid Temp: %s" % self.DELETEME)
        self.lblCausticTemp.set_label("Caustic Temp: %s" % self.DELETEME)

        self.DELETEME += 1

        return True

    def ProgressUpdater(self):
        if self.stopTimer:
            self.levelBar.set_value(0)
            self.lblStatus.set_label("IDLE")
            self.closeAll()
            self.readyToMoveOn = True
            return False
        if self.levelBar.get_value() < self.levelBar.get_max_value():
            self.levelBar.set_value(self.levelBar.get_value() + 1)
            self.readyToMoveOn = False
            return True
        else:
            self.levelBar.set_value(0)
            self.lblStatus.set_label("IDLE")
            self.closeAll()
            self.readyToMoveOn = True
            return False

    def closeAll(self):
        for button in [self.btnShutdown, self.btnRinse, self.btnCaustic,
                       self.btnAcid, self.btnSanitizer, self.btnO2Purge,
                       self.btnCO2Purge, self.btnCO2Pressurize]:
            button.set_sensitive(True)
            if button.get_active():
                button.activate()

        for switch in [self.switchWaterIn, self.switchWaterOut, self.switchCausticIn,
                       self.switchCausticOut, self.switchAcidIn, self.switchAcidOut,
                       self.switchSanitizerIn, self.switchSanitizerOut, self.switchPumpIn,
                       self.switchPumpPower, self.switchPumpOut, self.switchAir,
                       self.switchCO2]:
            if switch.get_active():
                switch.activate()

    def turnOffHeaters(self):
        if self.switchAcidHeater.get_active():
            self.switchAcidHeater.activate()
        if self.switchCausticHeater.get_active():
            self.switchCausticHeater.activate()

    def greyOutButtons(self):
        for button in [self.btnShutdown, self.btnRinse, self.btnCaustic,
                       self.btnAcid, self.btnSanitizer, self.btnO2Purge,
                       self.btnCO2Purge, self.btnCO2Pressurize]:
            button.set_sensitive(False)

    def unGreyOutButtons(self):
        for button in [self.btnShutdown, self.btnRinse, self.btnCaustic,
                       self.btnAcid, self.btnSanitizer, self.btnO2Purge,
                       self.btnCO2Purge, self.btnCO2Pressurize]:
            button.set_sensitive(True)

    def fullCycleSteps(self):
        if self.readyToMoveOn:
            if self.fullCycleProgess > NUMBER_OF_STEPS:
                self.unGreyOutButtons()
                self.fullCycleProgess = 1
                self.readyToMoveOn = True
                self.fullCycleRunning = False
                self.levelBar2.set_value(0)
                return False
            self.step[self.fullCycleProgess].set_sensitive(True)
            self.step[self.fullCycleProgess].activate()
            self.fullCycleProgess+=1
            self.levelBar2.set_value(self.fullCycleProgess)
            self.readyToMoveOn = False
        else:
            return True
#
# """
# HELPER FUNCTIONS STOP
# """
#
# """
# BUTTON FUNCTIONS START
# """

    def btnFullCycle_clicked(self, button):
        self.closeAll()
        self.greyOutButtons()
        self.fullCycleRunning = True
        GObject.timeout_add_seconds(1, self.fullCycleSteps)


    def btnAbort_clicked(self, button):
        self.stopTimer = True
        self.fullCycleProgess = 1
        self.levelBar2.set_value(0)
        self.closeAll()

    def btnRinse_clicked(self, button):
        if self.readyToMoveOn and self.fullCycleRunning: self.btnFullCycle.activate()
        if button.get_active():
            GObject.timeout_add_seconds(1, self.ProgressUpdater)
            if not self.switchPumpIn.get_active():
                self.switchPumpIn.activate()
            if not self.switchPumpPower.get_active():
                self.switchPumpPower.activate()
            if not self.switchPumpOut.get_active():
                self.switchPumpOut.activate()
            self.switchWaterIn.activate()
            self.switchWaterOut.activate()
            self.lblStatus.set_label("RINSE CYCLE")
            self.levelBar.set_max_value(RINSE_DURATION)
            self.stopTimer = False
        else:
            self.readyToMoveOn = True
            self.stopTimer = True
            self.lblStatus.set_label("IDLE")
            self.levelBar.set_value(0)

    def btnCaustic_clicked(self, button):
        if self.readyToMoveOn and self.fullCycleRunning: self.btnFullCycle.activate()
        if button.get_active():
            if not self.switchPumpIn.get_active():
                self.switchPumpIn.activate()
            if not self.switchPumpPower.get_active():
                self.switchPumpPower.activate()
            if not self.switchPumpOut.get_active():
                self.switchPumpOut.activate()
            self.switchCausticIn.activate()
            self.switchCausticOut.activate()
            self.lblStatus.set_label("CAUSTIC CYCLE")
            self.levelBar.set_max_value(CAUSTIC_DURATION)
            GObject.timeout_add_seconds(1, self.ProgressUpdater)
            self.stopTimer = False
        else:
            self.stopTimer = True
            self.lblStatus.set_label("IDLE")
            self.levelBar.set_value(0)

    def btnAcid_clicked(self, button):
        if self.readyToMoveOn and self.fullCycleRunning: self.btnFullCycle.activate()
        if button.get_active():
            if not self.switchPumpIn.get_active():
                self.switchPumpIn.activate()
            if not self.switchPumpPower.get_active():
                self.switchPumpPower.activate()
            if not self.switchPumpOut.get_active():
                self.switchPumpOut.activate()
            self.switchAcidIn.activate()
            self.switchAcidOut.activate()
            self.lblStatus.set_label("ACID CYCLE")
            self.levelBar.set_max_value(ACID_DURATION)
            GObject.timeout_add_seconds(1, self.ProgressUpdater)
            self.stopTimer = False
        else:
            self.stopTimer = True
            self.lblStatus.set_label("IDLE")
            self.levelBar.set_value(0)

    def btnSanitizer_clicked(self, button):
        if self.readyToMoveOn and self.fullCycleRunning: self.btnFullCycle.activate()
        if button.get_active():
            if not self.switchPumpIn.get_active():
                self.switchPumpIn.activate()
            if not self.switchPumpPower.get_active():
                self.switchPumpPower.activate()
            if not self.switchPumpOut.get_active():
                self.switchPumpOut.activate()
            self.switchSanitizerIn.activate()
            self.switchSanitizerOut.activate()
            self.lblStatus.set_label("SANITIZER CYCLE")
            self.levelBar.set_max_value(SANITIZER_DURATION)
            GObject.timeout_add_seconds(1, self.ProgressUpdater)
            self.stopTimer = False
        else:
            self.stopTimer = True
            self.lblStatus.set_label("IDLE")
            self.levelBar.set_value(0)

    def btnO2Purge_clicked(self, button):
        if self.readyToMoveOn and self.fullCycleRunning: self.btnFullCycle.activate()
        if button.get_active():
            self.switchAir.activate()
            self.switchWaterOut.activate()
            self.lblStatus.set_label("AIR PURGE CYCLE")
            self.levelBar.set_max_value(PURGE_DURATION)
            GObject.timeout_add_seconds(1, self.ProgressUpdater)
            self.stopTimer = False
        else:
            self.stopTimer = True
            self.lblStatus.set_label("IDLE")
            self.levelBar.set_value(0)

    def btnCO2Purge_clicked(self, button):
        if self.readyToMoveOn and self.fullCycleRunning: self.btnFullCycle.activate()
        if button.get_active():
            self.switchCO2.activate()
            self.switchWaterOut.activate()
            self.lblStatus.set_label("CO2 PURGE CYCLE")
            self.levelBar.set_max_value(PURGE_DURATION)
            GObject.timeout_add_seconds(1, self.ProgressUpdater)
            self.stopTimer = False
        else:
            self.stopTimer = True
            self.lblStatus.set_label("IDLE")
            self.levelBar.set_value(0)

    def btnCO2Pressurize_clicked(self, button):
        if self.readyToMoveOn and self.fullCycleRunning: self.btnFullCycle.activate()
        if button.get_active():
            if self.switchPumpIn.get_active():
                self.switchPumpIn.activate()
            if self.switchPumpPower.get_active():
                self.switchPumpPower.activate()
            if self.switchPumpOut.get_active():
                self.switchPumpOut.activate()
            self.switchCO2.activate()
            self.lblStatus.set_label("CO2 PRESSURIZE CYCLE")
            self.levelBar.set_max_value(PRESSURIZE_DURATION)
            GObject.timeout_add_seconds(1, self.ProgressUpdater)
            self.stopTimer = False
        else:
            self.stopTimer = True
            self.lblStatus.set_label("IDLE")
            self.levelBar.set_value(0)

    def btnShutdown_clicked(self, button):
        self.closeAll()
        self.turnOffHeaters()
        Gtk.main_quit()

# """
# BUTTON FUNCTIONS STOP
# """
#
# """
# SWITCH FUNCTIONS START
# """

    def switchWaterIn_state_set(self, switch, active):
        if active:
            print 'Water in solenoid activate'
        else:
            print 'Water out solenoid deactivate'

    def switchCausticIn_state_set(self, switch, active):
        if active:
            print 'Caustic in solenoid activate'
        else:
            print 'Caustic out solenoid deactivate'

    def switchAcidIn_state_set(self, switch, active):
        if active:
            print 'Acid in solenoid activate'
        else:
            print 'Acid out solenoid deactivate'

    def switchSanitizerIn_state_set(self, switch, active):
        if active:
            print 'Sanitizer in solenoid activate'
        else:
            print 'Sanitizer out solenoid deactivate'

    def switchPumpIn_state_set(self, switch, active):
        if active:
            print 'Pump in solenoid activate'
        else:
            print 'Pump out solenoid deactivate'

    def switchPumpPower_state_set(self, switch, active):
        if active:
            print 'Pump power solenoid activate'
        else:
            print 'Pump power solenoid deactivate'

    def switchPumpOut_state_set(self, switch, active):
        if active:
            print 'Pump out solenoid activate'
        else:
            print 'Pump out solenoid deactivate'

    def switchAir_state_set(self, switch, active):
        if active:
            print 'Air solenoid activate'
        else:
            print 'Ait solenoid deactivate'

    def switchCO2_state_set(self, switch, active):
        if active:
            print 'CO2 solenoid activate'
        else:
            print 'CO2 solenoid deactivate'

    def switchSanitizerOut_state_set(self, switch, active):
        if active:
            print 'Sanitizer out solenoid activate'
        else:
            print 'Sanitizer out solenoid deactivate'

    def switchAcidOut_state_set(self, switch, active):
        if active:
            print 'Acid Out solenoid activate'
        else:
            print 'Acid Out solenoid deactivate'

    def switchCausticOut_state_set(self, switch, active):
        if active:
            print 'Caustic out solenoid activate'
        else:
            print 'Caustic out solenoid deactivate'

    def switchWaterOut_state_set(self, switch, active):
        if active:
            print 'Water out solenoid activate'
        else:
            print 'Water out solenoid deactivate'

    def switchCausticHeater_state_set(self, switch, active):
        if active:
            print 'Caustic heater activate'
        else:
            print 'Caustic heater deactivate'

    def switchAcidHeater_state_set(self, switch, active):
        if active:
            print 'Acid heater activate'
        else:
            print 'Acid heater deactivate'

# """
# SWITCH FUNCTIONS STOP
# """


if __name__ == "__main__":
    gui = GuiGTK()
    Gtk.main()
