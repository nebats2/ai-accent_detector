# ai-accent_detector
An accent detector from a video.
<h1>OpenAI configuration</h1>
<p>Openai must be configured with the API key and preferred model. The default audio transcripter is whisper-1</p>
<br/>
<h3>Get Current openai configuraiton</h3>
GET /config/openai

<h3>Set openai configuraiton</h3>
POST /config/openai
{
  "url": "string",
  "api_key": "string",
  "model": "string",
  "transcription_model": "whisper-1"
}

<h1>Download video from web URL</h1>
POST /download/video/web <br/>

<p>If the video being downloaded is from the web, the URL must be provided and video must be downloaded before transcription</p><br/>

<h1>Download video from local (system)</h1>
POST /download/video/local/{url} <br/>
If the video is from the local system, use the local endpoint <br/>

<h1>Get accent rate</h1>
<p>The transcript extracts the text from the video and uses the openai prediction to provide the most probable accent of the speaker</p>
GET /accent/rate
