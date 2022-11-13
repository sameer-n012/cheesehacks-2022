export default function UploadForm() {

    return (
        <div>
            <h2>This is the upload page!</h2>
            <form method="POST" action="/api/upload" enctype="multipart/form-data">
                <input type="file" name="file" />
                <input type="submit" value="Upload" />
            </form>
        </div>
    )

}