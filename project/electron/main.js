const { app, BrowserWindow, Menu, ipcMain, nativeTheme} = require('electron');
const path = require('path');

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) { // eslint-disable-line global-require
  app.quit();
}

const createWindow = () => {
  global.meetings =[]
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
	  nodeIntegration: true,
      enableRemoteModule: true
    },
    backgroundColor: '#fcf1f1',
    // backgroundColor: '#D3D3D3',
    title: 'Elastic',
    show: false,
  });
  nativeTheme.themeSource ='light'
  //Quit app when closed
  mainWindow.on('closed', function() {
    app.quit;
  });

  // and load the index.html of the app.
  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  // Open the DevTools.
  mainWindow.webContents.openDevTools();

  mainWindow.webContents.on('did-finish-load', function () {
    mainWindow.show();
  });
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow);

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.


// const {Meeting} =require('./Model/Meeting');

// function loadMeetings() {
//   database.count({}, function (err, count) {
//     if(count !=0) {
//       database.find({}, function (err, docs) {
//         for(var i =0; i <docs.length; i++) {
//           global.meetings.push(new Meeting(docs[i].meetingName, docs[i].meetingID, docs[i].meetingPassword, docs[i].weekDays,
//               docs[i].meetingStartTime, docs[i].meetingEndTime))
//         }
//       })
//     }
//   })
// }
// ipcMain.on("pushMeeting", ( event, meetingName,meetingID,meetingPassword,weekDays,meetingStartTime,meetingEndTime) => {
//   global.meetings.push(new Meeting(meetingName,meetingID,meetingPassword,weekDays,meetingStartTime,meetingEndTime))

//   database.insert({meetingName: meetingName, meetingID: meetingID, meetingPassword: meetingPassword, weekDays: weekDays,
//     meetingStartTime: meetingStartTime, meetingEndTime: meetingEndTime})
// });
// ipcMain.on('setEditMeetingIndex', (event, i) => {
//   global.editMeetingIndex =i
// });
// ipcMain.on('getEditMeeting', (event, arg) => {
//   event.returnValue =global.meetings[global.editMeetingIndex];
// })
// ipcMain.on('getMeetings', (event, arg) => {
//   event.returnValue =global.meetings;
// });
// ipcMain.on('getMeetingAt', (event, arg) => {
//   event.returnValue =global.meetings[arg];
// });
// ipcMain.on('openMeeting', (event, i) => {
//   global.meetings[i].openMeeting();
// });
// ipcMain.on('popMeeting', (event, i) => {
//   global.meetings.splice(i,1);
// });
// ipcMain.on('addWeekDay', (event, i, day) => {
//   global.meetings[i].days.push(day);
//   database.update({meetingID: global.meetings[i].meetingID}, {$set: {weekDays: global.meetings[i].days}}, function (err, numReplaced) {});
//   database.persistence.compactDatafile()
// });
// ipcMain.on('deleteWeekDay', (event, i, day) => {
//   d =global.meetings[i].days
//   global.meetings[i].days.splice(d.indexOf(day),1)
//   database.update({meetingID: global.meetings[i].meetingID}, {$set: {weekDays: d}}, function (err, numReplaced) {});
//   database.persistence.compactDatafile()
// });
// ipcMain.on('deleteMeeting', (event) => {
//   database.remove({meetingID: global.meetings[global.editMeetingIndex].meetingID}, function (err, numReplaced) {});
//   database.persistence.compactDatafile()
//   global.meetings.splice(global.editMeetingIndex,1)
// });
// ipcMain.on('updateMeeting', (event, meetingName,meetingID,meetingPassword,meetingStartTime,meetingEndTime) => {
//   const i =global.editMeetingIndex;

//   database.update({meetingID: global.meetings[i].meetingID}, {$set: {meetingName: meetingName,meetingID: meetingID, meetingPassword: meetingPassword, meetingStartTime: meetingStartTime, meetingEndTime: meetingEndTime}}, function (err, numReplaced) {});
//   database.persistence.compactDatafile()

//   global.meetings[i].name =meetingName
//   global.meetings[i].meetingID =meetingID
//   global.meetings[i].password =meetingPassword
//   global.meetings[i].startTime =meetingStartTime
//   global.meetings[i].endTime =meetingEndTime
// });