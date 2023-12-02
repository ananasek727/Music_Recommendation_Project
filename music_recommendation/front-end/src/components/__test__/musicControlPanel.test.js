import {configure} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import {shallow} from 'enzyme';
import MusicControlPanel from "../MusicControlPanel";


configure({adapter: new Adapter()});

it('should render without errors', () => {
    const props = {};
    const wrapper = shallow(<MusicControlPanel {...props} />);

    expect(wrapper).toBeTruthy();
});
it('should display four buttons for controlling music playback', () => {
    const props = {};
    const wrapper = shallow(<MusicControlPanel {...props} />);
    expect(wrapper.find('button')).toHaveLength(4);
});
it('should send a POST request to the Spotify API to play the previous track when the \'Previous track\' button is clicked', () => {

  const props = {};
  const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValueOnce({});

  const wrapper = shallow(<MusicControlPanel {...props} />);
  wrapper.find('button').at(0).simulate('click');

  expect(fetchMock).toHaveBeenCalledWith(`https://api.spotify.com/v1/me/player/previous?device_id=`, {
    method: "POST",
    headers: {
      Authorization: `Bearer `,
    },
  });
});


