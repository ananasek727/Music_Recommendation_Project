import {configure} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import MusicControl from "../MusicControl";
import {shallow} from 'enzyme';

configure({adapter: new Adapter()});
it('should render a div with class \'MusicControlFrame\'', () => {
    const playlist = {
        name: "My Playlist",
        songs: [
            {
                title: "Song 1",
                artist: "Artist 1",
                duration: 200,
                image_url: "image1.jpg",
                id: "1",
                uri: "1",
            },
            {
                title: "Song 2",
                artist: "Artist 2",
                duration: 180,
                image_url: "image2.jpg",
                id: "2",
                uri: "2",
            },
            {
                title: "Song 3",
                artist: "Artist 3",
                duration: 220,
                image_url: "image3.jpg",
                id: "3",
                uri: "3",
            },
        ]
    };

    const wrapper = shallow(<MusicControl playlist={playlist}/>);
    expect(wrapper.find('.MusicControlFrame')).toHaveLength(1);
});
it('should render a div with class \'MusicControlPlaylistHolder\'', () => {
    const playlist = {
        name: "My Playlist",
        songs: [
            {
                title: "Song 1",
                artist: "Artist 1",
                duration: 200,
                image_url: "image1.jpg",
                id: "1",
                uri: "1",
            },
            {
                title: "Song 2",
                artist: "Artist 2",
                duration: 180,
                image_url: "image2.jpg",
                id: "2",
                uri: "2",
            },
            {
                title: "Song 3",
                artist: "Artist 3",
                duration: 220,
                image_url: "image3.jpg",
                id: "3",
                uri: "3",
            },
        ]
    };

    const wrapper = shallow(<MusicControl playlist={playlist}/>);
    expect(wrapper.find('.MusicControlPlaylistHolder')).toHaveLength(1);
});
it('should render a div with class \'MusicControlPlaybackHolder\'', () => {
    const playlist = {
        name: "My Playlist",
        songs: [
            {
                title: "Song 1",
                artist: "Artist 1",
                duration: 200,
                image_url: "image1.jpg",
                id: "1",
                uri: "1",
            },
            {
                title: "Song 2",
                artist: "Artist 2",
                duration: 180,
                image_url: "image2.jpg",
                id: "2",
                uri: "2",
            },
            {
                title: "Song 3",
                artist: "Artist 3",
                duration: 220,
                image_url: "image3.jpg",
                id: "3",
                uri: "3",
            },
        ]
    };

    const wrapper = shallow(<MusicControl playlist={playlist}/>);
    expect(wrapper.find('.MusicControlPlaybackHolder')).toHaveLength(1);
});
it('should not render a PlaylistElement if the playlist is empty', () => {
    const playlist = {
        name: "My Playlist",
        songs: []
    };

    const wrapper = shallow(<MusicControl playlist={playlist}/>);
    expect(wrapper.find('PlaylistElement')).toHaveLength(0);
});