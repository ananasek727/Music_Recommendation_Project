import {shallow} from 'enzyme';
import {configure, simulate, text} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import MusicRecommendationPage from "../MusicRecommendation";

configure({adapter: new Adapter()});

it('should render the component with default state and display the Emotion recognition section, Music recommendation parameters section, and Music control section', () => {
    // Arrange

    // Act
    const wrapper = shallow(<MusicRecommendationPage/>);

    // Assert
    expect(wrapper.find('.mRPageFrame')).toHaveLength(1);
    expect(wrapper.find('.mRPageBoxLeft')).toHaveLength(1);
    expect(wrapper.find('.mRPageBoxLeftDecisionButtonFrame')).toHaveLength(1);
    expect(wrapper.find('.mRPageBoxLeftDecisionButton')).toHaveLength(2);
    expect(wrapper.find('.mRPageBoxLeftWebCamFrame')).toHaveLength(0);
    expect(wrapper.find('.mRPageBoxLeftUploadFrame')).toHaveLength(0);
    expect(wrapper.find('.MRPageBoxLeftParametersFrame')).toHaveLength(1);
    expect(wrapper.find('.mRPageBoxLeftText').at(1).text()).toBe('Music recommendation parameters');
    expect(wrapper.find('MusicParameters')).toHaveLength(1);
    expect(wrapper.find('.mRPageBoxRight')).toHaveLength(1);
    expect(wrapper.find('MusicControl')).toHaveLength(1);
});


it('should display the default sample playlist when the component is rendered', () => {
    // Arrange
    const wrapper = shallow(<MusicRecommendationPage/>);

    // Act

    // Assert
    expect(wrapper.find('MusicControl').prop('playlist')).toEqual({
        name: "Sample playlist",
        songs: [
            {
                title: "Post",
                artist: "Dawid Podsiadło",
                duration: 100000,
                image_url: "123",
                id: "1",
                uri: "1",
            },
            {
                title: "To co masz Ty!",
                artist: "Dawid Podsiadło",
                duration: 100000,
                image_url: "1234",
                id: "2",
                uri: "2",
            }
        ]
    });
});

it('should display the default sample playlist when the selected music recommendation parameters do not match any playlist', () => {
    // Arrange
    const wrapper = shallow(<MusicRecommendationPage/>);
    wrapper.find('MusicParameters').prop('setMusicParameter1')('parameter1');
    wrapper.find('MusicParameters').prop('setMusicParameter2')('parameter2');
    wrapper.find('MusicParameters').prop('setMusicParameter3')('parameter3');

    // Act

    // Assert
    expect(wrapper.find('MusicControl').prop('playlist')).toEqual({
        name: "Sample playlist",
        songs: [
            {
                title: "Post",
                artist: "Dawid Podsiadło",
                duration: 100000,
                image_url: "123",
                id: "1",
                uri: "1",
            },
            {
                title: "To co masz Ty!",
                artist: "Dawid Podsiadło",
                duration: 100000,
                image_url: "1234",
                id: "2",
                uri: "2",
            }
        ]
    });
});