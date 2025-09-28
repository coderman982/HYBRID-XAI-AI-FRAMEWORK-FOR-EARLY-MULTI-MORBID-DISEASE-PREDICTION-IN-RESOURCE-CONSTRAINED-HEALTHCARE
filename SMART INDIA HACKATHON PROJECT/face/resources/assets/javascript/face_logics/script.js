var labels = [];
let detectedFaces = [];
let sendingData = false;

function updateTable() {
  var selectedCourseID = document.getElementById("courseSelect").value;
  var selectedUnitCode = document.getElementById("unitSelect").value;
  var selectedVenue = document.getElementById("venueSelect").value;
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "resources/pages/lecture/manageFolder.php", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var response = JSON.parse(xhr.responseText);
      if (response.status === "success") {
        labels = response.data;

        if (selectedCourseID && selectedUnitCode && selectedVenue) {
          updateOtherElements();
        }
        document.getElementById("studentTableContainer").innerHTML =
          response.html;
      } else {
        console.error("Error:", response.message);
      }
    }
  };
  xhr.send(
    "courseID=" +
      encodeURIComponent(selectedCourseID) +
      "&unitID=" +
      encodeURIComponent(selectedUnitCode) +
      "&venueID=" +
      encodeURIComponent(selectedVenue)
  );
}

function markAttendance(detectedFaces) {
  document.querySelectorAll("#studentTableContainer tr").forEach((row) => {
    const registrationNumber = row.cells[0].innerText.trim();
    if (detectedFaces.includes(registrationNumber)) {
      row.cells[5].innerText = "present";
    }
  });
}

function updateOtherElements() {
  const video = document.getElementById("video");
  const videoContainer = document.querySelector(".video-container");
  const startButton = document.getElementById("startButton");
  let webcamStarted = false;
  let modelsLoaded = false;

  // Resolve models directory robustly whether app is at / or /face
  const appBaseSegment = window.location.pathname.startsWith('/face/') || window.location.pathname === '/face'
    ? '/face'
    : '';
  const MODELS_URL = `${appBaseSegment}/models`;

  Promise.all([
    faceapi.nets.ssdMobilenetv1.loadFromUri(MODELS_URL),
    faceapi.nets.faceRecognitionNet.loadFromUri(MODELS_URL),
    faceapi.nets.faceLandmark68Net.loadFromUri(MODELS_URL),
  ])
    .then(() => {
      modelsLoaded = true;
      console.log("models loaded successfully");
    })
    .catch(() => {
      alert("models not loaded, please check your model folder location");
    });
  startButton.addEventListener("click", async () => {
    videoContainer.style.display = "flex";
    if (!webcamStarted && modelsLoaded) {
      startWebcam();
      webcamStarted = true;
    }
  });

  function startWebcam() {
    navigator.mediaDevices
      .getUserMedia({
        video: true,
        audio: false,
      })
      .then((stream) => {
        video.srcObject = stream;
        videoStream = stream;
      })
      .catch((error) => {
        console.error(error);
      });
  }
  async function getLabeledFaceDescriptions() {
    const labeledDescriptors = [];
    console.log('=== FACE RECOGNITION DEBUG ===');
    console.log('Loading face descriptions for students:', labels);
    console.log('Number of students to process:', labels.length);

    if (labels.length === 0) {
      console.error('❌ NO STUDENTS FOUND! Make sure you have:');
      console.error('1. Selected a course, unit, and venue');
      console.error('2. Added students to the database');
      console.error('3. Added student face images to resources/labels/');
      return labeledDescriptors;
    }

    for (const label of labels) {
      const descriptions = [];
      console.log(`\n--- Processing student: ${label} ---`);

      // Try common image file patterns that cameras and websites use
      const commonImageNames = [
        // Numbered patterns
        '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg',
        '1.png', '2.png', '3.png', '4.png', '5.png',
        '1.jpeg', '2.jpeg', '3.jpeg', '4.jpeg', '5.jpeg',
        
        // Camera default names
        'IMG_001.jpg', 'IMG_002.jpg', 'IMG_003.jpg', 'IMG_004.jpg', 'IMG_005.jpg',
        'IMG_001.png', 'IMG_002.png', 'IMG_003.png', 'IMG_004.png', 'IMG_005.png',
        
        // Photo names
        'photo1.jpg', 'photo2.jpg', 'photo3.jpg', 'photo4.jpg', 'photo5.jpg',
        'photo1.png', 'photo2.png', 'photo3.png', 'photo4.png', 'photo5.png',
        
        // Simple names
        'image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.jpg',
        'image1.png', 'image2.png', 'image3.png', 'image4.png', 'image5.png',
        
        // Webcam names
        'webcam1.jpg', 'webcam2.jpg', 'webcam3.jpg', 'webcam4.jpg', 'webcam5.jpg',
        'webcam1.png', 'webcam2.png', 'webcam3.png', 'webcam4.png', 'webcam5.png',
        
        // Generic names
        'face1.jpg', 'face2.jpg', 'face3.jpg', 'face4.jpg', 'face5.jpg',
        'face1.png', 'face2.png', 'face3.png', 'face4.png', 'face5.png'
      ];
      
      let imagesFound = 0;
      const maxImages = 5;
      
      for (const imageName of commonImageNames) {
        if (imagesFound >= maxImages) break;
        
        try {
          const imagePath = `resources/labels/${label}/${imageName}`;
          console.log(`Trying to load: ${imagePath}`);
          
          const img = await faceapi.fetchImage(imagePath);
          const detections = await faceapi
            .detectSingleFace(img)
            .withFaceLandmarks()
            .withFaceDescriptor();

          if (detections) {
            descriptions.push(detections.descriptor);
            console.log(`✓ Face detected in ${label}/${imageName}`);
            imagesFound++;
          } else {
            console.log(`✗ No face detected in ${label}/${imageName}`);
          }
        } catch (error) {
          // Image not found or error loading - continue to next
          continue;
        }
      }
      
      if (imagesFound === 0) {
        console.error(`❌ No valid images found for student ${label}`);
        console.error('Please add image files to: resources/labels/' + label + '/');
        console.error('Supported names: 1.jpg, 2.jpg, IMG_001.jpg, photo1.jpg, etc.');
      } else {
        console.log(`✓ Found ${imagesFound} valid images for ${label}`);
        if (imagesFound < 5) {
          console.warn(`⚠️ For best results, add 5 images for ${label}`);
        }
      }

      if (descriptions.length > 0) {
        labeledDescriptors.push(
          new faceapi.LabeledFaceDescriptors(label, descriptions)
        );
        console.log(`✓ Student ${label}: ${descriptions.length} valid face descriptions loaded`);
      } else {
        console.warn(`❌ No valid face descriptions found for student: ${label}`);
        console.warn('Make sure you have 5 clear face images in: resources/labels/' + label + '/');
      }
    }

    console.log(`\n=== SUMMARY ===`);
    console.log(`Total students with valid face data: ${labeledDescriptors.length}`);
    if (labeledDescriptors.length === 0) {
      console.error('❌ NO FACE DATA LOADED! Face recognition will not work.');
      console.error('To fix this:');
      console.error('1. Add student face images to resources/labels/{registrationNumber}/');
      console.error('2. Each student needs 5 images named: 1.png, 2.png, 3.png, 4.png, 5.png');
      console.error('3. Images should be clear, well-lit face photos');
    } else {
      console.log('✓ Face recognition system is ready!');
    }
    return labeledDescriptors;
  }

  video.addEventListener("play", async () => {
    const labeledFaceDescriptors = await getLabeledFaceDescriptions();
    const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors);

    const canvas = faceapi.createCanvasFromMedia(video);
    videoContainer.appendChild(canvas);

    const displaySize = { width: video.width, height: video.height };
    faceapi.matchDimensions(canvas, displaySize);

    setInterval(async () => {
      const detections = await faceapi
        .detectAllFaces(video)
        .withFaceLandmarks()
        .withFaceDescriptors();

      const resizedDetections = faceapi.resizeResults(detections, displaySize);

      canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);

      const results = resizedDetections.map((d) => {
        return faceMatcher.findBestMatch(d.descriptor);
      });
      
      // Filter out unknown faces and get only recognized students
      detectedFaces = results
        .filter((result) => result.label !== 'unknown' && result.distance < 0.6)
        .map((result) => result.label);
      
      console.log('=== FACE DETECTION RESULTS ===');
      console.log('Total faces detected:', results.length);
      console.log('Recognition results:', results.map(r => ({label: r.label, distance: r.distance.toFixed(3)})));
      console.log('Recognized students (distance < 0.6):', detectedFaces);
      
      if (detectedFaces.length > 0) {
        console.log('✓ Marking attendance for:', detectedFaces);
        markAttendance(detectedFaces);
      } else if (results.length > 0) {
        console.log('⚠️ Faces detected but not recognized. Check:');
        console.log('1. Are student face images properly loaded?');
        console.log('2. Is the face clear and well-lit?');
        console.log('3. Are you looking directly at the camera?');
      } else {
        console.log('No faces detected in the current frame');
      }

      results.forEach((result, i) => {
        const box = resizedDetections[i].detection.box;
        const drawBox = new faceapi.draw.DrawBox(box, {
          label: result,
        });
        drawBox.draw(canvas);
      });
    }, 100);
  });
}

function sendAttendanceDataToServer() {
  const attendanceData = [];

  document
    .querySelectorAll("#studentTableContainer tr")
    .forEach((row, index) => {
      const studentID = row.cells[0].innerText.trim();
      const course = row.cells[2].innerText.trim();
      const unit = row.cells[3].innerText.trim();
      const attendanceStatus = row.cells[5].innerText.trim();

      // Only save students who were marked as "present" by face recognition
      if (attendanceStatus.toLowerCase() === "present") {
        attendanceData.push({ studentID, course, unit, attendanceStatus });
        console.log(`✓ Saving attendance for ${studentID}: ${attendanceStatus}`);
      } else {
        console.log(`⚠️ Skipping ${studentID}: ${attendanceStatus} (not present)`);
      }
    });

  console.log(`Total students to save: ${attendanceData.length}`);
  if (attendanceData.length === 0) {
    showMessage("No students were marked as present. No attendance data to save.");
    return;
  }

  const xhr = new XMLHttpRequest();
  const appBaseSegment = window.location.pathname.startsWith('/face/') || window.location.pathname === '/face'
    ? '/face'
    : '';
  const ATTENDANCE_URL = `${appBaseSegment}/resources/pages/lecture/handle_attendance.php`;
  xhr.open("POST", ATTENDANCE_URL, true);
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        try {
          const response = JSON.parse(xhr.responseText);

          if (response.status === "success") {
            showMessage(
              response.message || "Attendance recorded successfully."
            );
          } else {
            showMessage(
              response.message ||
                "An error occurred while recording attendance."
            );
          }
        } catch (e) {
          showMessage("Error: Failed to parse the response from the server.");
          console.error(e);
        }
      } else {
        showMessage(
          "Error: Unable to record attendance. HTTP Status: " + xhr.status
        );
        console.error("HTTP Error", xhr.status, xhr.statusText);
      }
    }
  };

  xhr.send(JSON.stringify(attendanceData));
}
function showMessage(message) {
  var messageDiv = document.getElementById("messageDiv");
  messageDiv.style.display = "block";
  messageDiv.innerHTML = message;
  console.log(message);
  messageDiv.style.opacity = 1;
  setTimeout(function () {
    messageDiv.style.opacity = 0;
  }, 5000);
}
function stopWebcam() {
  if (videoStream) {
    const tracks = videoStream.getTracks();

    tracks.forEach((track) => {
      track.stop();
    });

    video.srcObject = null;
    videoStream = null;
  }
}

document.getElementById("endAttendance").addEventListener("click", function () {
  sendAttendanceDataToServer();
  const videoContainer = document.querySelector(".video-container");
  videoContainer.style.display = "none";
  stopWebcam();
});
