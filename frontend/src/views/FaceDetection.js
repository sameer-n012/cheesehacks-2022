import {useEffect, useRef, useState} from 'react'

export default function FaceDetection() {

	const UPLOADS_PER_SECOND = 10

	// OVERALL FLOW:
	// useEffect at the start triggers camera feed
	const videoRef = useRef();
	const inputRef = useRef();
	const canvasRef = useRef();
	const imageRef = useRef();

	useEffect(() => {
		startVideo()
		getImageFromVideo()
	}, [])

	async function startVideo() {
		try {
			const stream = await navigator.mediaDevices.getUserMedia({ video: true })
			videoRef.current.srcObject = stream
		}
		catch(err) {
			console.log('Error while starting video stream')
			console.error(err)
		}
	}

	function captureVideo(videoElem) {
		const canvas = document.createElement("canvas");
		canvas.width = videoElem.videoWidth;
		canvas.height = videoElem.videoHeight;
		const canvasContext = canvas.getContext("2d");
		canvasContext.drawImage(videoElem, 0, 0);
		return canvas.toDataURL('image/png');	
	}

	function getImageFromVideo() {

		setInterval( () => {
			
			//console.log('inside getImage function: ' + JSON.stringify(image))
			sendImage(captureVideo(videoRef.current))

		}, 1000 / UPLOADS_PER_SECOND)
		
	}

	async function sendImage(img) {

		const classCode = inputRef.current.value
		const formData = new FormData()
		formData.append('image', img)
		const requestOptions = {
			method: 'POST',
			body: formData
		}
		if (classCode) { // Truthy check, see if classCode is not empty string
			const rawRes = await fetch('/api/detect/' + classCode, requestOptions)
			const textRes = await rawRes.text()
			console.log(`json response: ${textRes}`)
		}

	}


	return (
		<div>
			<h1>This is the face detection page</h1>
			<label htmlFor='class-code-input'>Type in your class code</label>
			<input id="class-code-input" ref={inputRef} placeholder='Class code'/>
			<div className='detector-area'>
				<div className='detector-video'>
					<video crossOrigin='anonymous' ref={videoRef} id="detect-video" autoPlay ></video>
				</div>
				<canvas ref={canvasRef}></canvas>
				<img ref={imageRef}/>
            </div>
		</div>
	);
}
