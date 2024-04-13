/*
AR_ImportSRT

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ImportSRT
Description-US: Imports subtitles (SRT) file and creates text layers with specific settings.
Written for Adobe After Effects CC 2019 (Version 16.0.1 Build 48)

*/
//@target aftereffects
function TimeToFrames(time, comp) {
    var frames = time * (1.0 / comp.frameDuration);
    return frames;
}
function FramesToTime(frames, comp) {
    var time = frames / (1.0 / comp.frameDuration);
    return time;
}
function Time(timeInString) {
    var t = timeInString.split(":");
    var s = parseInt(t[0])*3600 + parseInt(t[1])*60 + parseFloat(t[2].replace(",","."));
    return s;
}
function ImportSRT() {
    app.beginUndoGroup("AR_ImportSRT"); // Begin undo group
    var comp = app.project.activeItem; // Get active composition
    if (comp instanceof CompItem){ // Check that there really is composition
        var srt = File.openDialog("Select a text file to open.", "SRT subtitles:*.srt"); // Prompt to load srt file
        if (srt != null) { // Check that there is file
            srt.open("r"); // Open file for reading
            while (!srt.eof) { // Go through subtitle file's lines
                var layer = comp.layers.addText("SRT"); // Add text layer
                var sourceText = layer.property("sourceText"); // Get property
                var textDocument = sourceText.value; // Get the current text document
                var line = srt.readln(); // Read line from the file
                while (line == "") { // Skip empty lines
                    line = srt.readln();
                }
                    line = srt.readln();
                var times = line.split("-->"); // Get timecode
                var f = Time(times[0]); // Get in time
                var l = Time(times[1]); // Get out time
                var text = ""; // Initialize text string
                while ((line = srt.readln()) != "") { // Handle text
                    text += line.replace(/<(.*?)>/g, "")+"\r\n";
                }
                textDocument.text = text; // Set text
                textDocument.font = "Calibri-Bold"; // Set font
                textDocument.fontSize = 34; // Set font size
                textDocument.justification = ParagraphJustification.CENTER_JUSTIFY; // Set text alignment
                sourceText.setValue(textDocument); // Update the source text property

                var inFrame = TimeToFrames(f, comp);
                var outFrame = TimeToFrames(l, comp);
                var roundedInFrame = Math.round(inFrame);
                var roundedOutFrame = Math.round(outFrame);
                var inTime = FramesToTime(roundedInFrame, comp);
                var outTime = FramesToTime(roundedOutFrame, comp);

                layer.inPoint = inTime; // Set layer in point
                layer.outPoint = outTime; // Set layer out point
                layer.position.setValue([639.5, 708]); // Set position of the text layer
            }
            srt.close(); // Close file
        }
    } else { // If something went wrong
        alert("Make a comp first."); // Alert user
    }    
    app.endUndoGroup(); // End undo group
}
ImportSRT(); // Run import subtitles function
