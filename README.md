# Yandex-Music-Playlist-To-Spotify-Playlist
 This Python script transforms your Yandex.Music vibes into Spotify playlists effortlessly. Choose your mood - whether it's "Playlist of the Day," "Deja Vu," or "Premiere" - and watch as the magic unfolds. With just a few clicks, groove to your favorite tunes seamlessly across platforms.

## Usage Instructions:

1. **Create an application on Spotify Dashboard**:
   - Go to [Spotify Dashboard](https://developer.spotify.com/dashboard/applications).
   - Click on "Create App".
   - Fill in the fields "App name" and "App description".
   - The "Website" field does not need to be filled, in the "Redirect URI" field, specify the `redirect_uri` from the `config.json` file: `http://localhost:8888/callback`.
   - Enable the "Web API" checkbox.
   - Agree to Spotify's terms and conditions and click "Save".
   - Go to "Settings".
   - In the "Basic Information" section, copy the "Client ID" and "Client Secret" and paste them into the `config.json` file in the corresponding fields: `client_id`, `client_secret`.

2. **Enter your data into `config.json`**:
   - Open the `config.json` file and fill it with your data.

3. **Like playlists on Yandex.Music**:
   - Like the playlists "Playlist of the Day," "Deja Vu," and "Premiere" in your Yandex.Music account.

4. **Get the Yandex Token and add it to `config.json`**:
   - Install the [Yandex Music Token](https://chromewebstore.google.com/detail/yandex-music-token/lcbjeookjibfhjjopieifgjnhlegmkib) extension for Google Chrome.
   - Log in to your Yandex account.
   - Click on the "Copy token" button.
   - Paste the copied token into the `yandex_token` field of the `config.json` file.

That's it! Now you can run the script to create Spotify playlists based on Yandex.Music playlists.
