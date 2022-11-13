import UploadForm from "./UploadForm";
import './StudentUpload.css'

export default function StudentUpload() {
	return (
		<div className="student_upload">
			<h2 className="upload-header">Upload a picture of yourself!</h2>
			<UploadForm />
		</div>
	);
}
