import * as React from 'react';
import styles from './css/MusicParameters.module.css';
import { Theme, useTheme } from '@mui/material/styles';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

function getStyles(name: string, personName: string[], theme: Theme) {
  return {
    fontWeight:
      personName.indexOf(name) === -1
        ? theme.typography.fontWeightRegular
        : theme.typography.fontWeightMedium,
  };
}

const Genres = [
  'pop',
  'rock',
  'indie',
];

function MusicParameters  (props: any)  {

    // get recommended playlist
    const handlePlaylistRecommendation = async () => {

        await fetch(`http://127.0.0.1:8000/create-playlist-based-on-parameters`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                "emotion": props.detectedEmotion,
                "personalization": props.musicParameter2,
                "popularity": props.musicParameter1,
                "genres": props.musicParameter3
              })
              })
              .then((response) => {
                if (response.ok) return response.json();
                else {
                  throw new Error("ERROR " + response.status);
                }
              })
              .then((data) => {
                props.setRecommendedPlaylist(data);
                console.log(data);
                const allURI: string[] = data.data.map((item: { uri: any; }) => item.uri);
                props.setPlaylistSongURI(allURI);
                console.log(allURI);
                props.setIsPlaylistEmpty(false);
                props.setPlaylistChangeGuard(!props.playlistChangeGuard);
              })
              .catch((e) => {
                console.log("Error when trying to get recommended playlist: " + e);
              });
      }

      // save playlist
    const savePlaylist = async () => {
      await fetch(`http://127.0.0.1:8000/save-playlist`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              "name": "Mus4You"
            })
          })
          .then((response) => {
            if (response.ok) return response.json();
            else {
              throw new Error("ERROR " + response.status);
            }
          })
          .catch((e) => {
          console.log("Error when trying to save playlist: " + e);
          });   
    }

    const handleChangePopularity = (event: SelectChangeEvent) => {
        props.setMusicParameter1(event.target.value);
    };

    const handleChangePersonalization = (event: SelectChangeEvent) => {
        props.setMusicParameter2(event.target.value);
    };

    const [personName, setPersonName] = React.useState<string[]>([]);
    const theme = useTheme();

    const handleChangeGenres = (event: SelectChangeEvent<typeof props.musicParameter3>) => {
      const {
        target: { value },
      } = event;
      props.setMusicParameter3(event.target.value);
    };

    return (
        <div className={styles.MusicParametersBox}>
            <div className={styles.MusicParametersSpaceHolder} />
            {/* Popularity */}
            <FormControl sx={{ m: 1, minWidth: 130 }} size="small">
              <InputLabel>Popularity</InputLabel>
              <Select
                data-testid="popularity-select"
                value={props.musicParameter1}
                label="Popularity"
                onChange={handleChangePopularity}
              >
                <MenuItem value="">
                  <em>None</em>
                </MenuItem>
                <MenuItem value="mainstream">Mainstream</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="low">Low</MenuItem>
              </Select>
            </FormControl>
            {/* <select className={styles.MusicParametersSelect} value={props.musicParameter1} onChange={handleChangePopularity}>
                <option value="">Popularity</option>
                <option value="mainstream">Mainstream</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
            </select> */}
            {/* Personalization level */}
            <FormControl sx={{ m: 1, minWidth: 160 }} size="small">
              <InputLabel >Personalization</InputLabel>
              <Select
                data-testid="personalization-select"
                value={props.musicParameter2}
                label="Personalization"
                onChange={handleChangePersonalization}
              >
                <MenuItem value="">
                  <em>None</em>
                </MenuItem>
                <MenuItem value="high">High</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="low">Low</MenuItem>
              </Select>
            </FormControl>
            {/* <select className={styles.MusicParametersSelect} value={props.musicParameter2} onChange={handleChangePersonalization}>
                <option value="">Personalization</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
            </select> */}
            {/* Genres */}
            <FormControl sx={{ m: 1, minWidth: 100 }} size="small">
            <InputLabel>Genres</InputLabel>
            <Select
              data-testid="genres-select"
              multiple
              value={props.musicParameter3}
              onChange={handleChangeGenres}
              input={<OutlinedInput label="Genres" />}
              MenuProps={MenuProps}
            >
              {Genres.map((genre) => (
                <MenuItem
                  key={genre}
                  value={genre}
                  style={getStyles(genre, props.musicParameter2, theme)}
                >
                  {genre}
                </MenuItem>
              ))}
            </Select>
            </FormControl>
            {(props.musicParameter1 != '' && props.musicParameter2 != '' && props.musicParameter3.length > 0 && props.detectedEmotion != '') ?
            <button className={styles.MusicParametersButton} onClick={handlePlaylistRecommendation}>Recommend music</button>
            :
            <button className={styles.MusicParametersButton} onClick={handlePlaylistRecommendation} disabled={true}>Recommend music</button>
            }
            <button className={styles.MusicParametersButton} onClick={savePlaylist} disabled={props.isPlaylistEmpty}>Save playlist</button>
        </div>
    )
  };

  export default MusicParameters;