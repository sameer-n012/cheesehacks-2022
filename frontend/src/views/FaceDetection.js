import {useEffect, useRef, useState} from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom';
import './FaceDetection.css'

export default function FaceDetection() {

	const navigate = useNavigate();

	const [searchParams, _] = useSearchParams();
	const [classCode, setClassCode] = useState('')
	useEffect(() => {
		setClassCode(searchParams.get('classCode'))
	}, [])

	const UPLOADS_PER_SECOND = 5

	// OVERALL FLOW:
	// useEffect at the start triggers camera feed
	const videoRef = useRef();

	const [responseMsg, setResponseMsg] = useState('')

	useEffect(() => {
		startVideo()
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

	useEffect(() => {

		setInterval( () => {

			if (classCode) {
				sendImage(captureVideo(videoRef.current))
			}

		}, 1000 / UPLOADS_PER_SECOND)
		
	}, [classCode])

	async function sendImage(img) {

		const formData = new FormData()
		formData.append('image', img)
		const requestOptions = {
			method: 'POST',
			body: formData
		}
		const rawRes = await fetch('/api/detect/' + classCode, requestOptions)
		const textRes = await rawRes.text()
		setResponseMsg("Found: " + textRes)

	}


	return (
		<div className="face-dec-page-wrapper">
			<h2 className="face-dec-title">Face detection for class {classCode}</h2>
			<div className='detector-area'>
				<div className='detector-video'>
					<video crossOrigin='anonymous' ref={videoRef} id="detect-video" autoPlay></video>
				</div>
				<p className="response-msg">{responseMsg}‎ </p>
            </div>
			<button onClick={()=>{navigate('/student')}} className="btn btn-outline-dark w-25 m-3">Back</button>
		</div>
	);
}
