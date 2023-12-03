import {shallow} from 'enzyme';
import WebCamFrame from "../WebCamFrame";
import {configure} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({adapter: new Adapter()});
it('should render a div with class WebCamFrameBox', () => {
    // Arrange
    const props = {
        imgSrc: null,
        width: 100,
        height: 100,
        setImgSrc: jest.fn()
    };

    // Act
    const wrapper = shallow(<WebCamFrame {...props} />);

    // Assert
    expect(wrapper.find('.WebCamFrameBox')).toHaveLength(1);
});
it('should render a button with class webCamFrameButton', () => {
    // Arrange
    const props = {
        imgSrc: null,
        width: 100,
        height: 100,
        setImgSrc: jest.fn()
    };

    // Act
    const wrapper = shallow(<WebCamFrame {...props} />);

    // Assert
    expect(wrapper.find('.webCamFrameButton')).toHaveLength(1);
});
it('should render an img tag with class WebCamFrameImg and src equal to props.imgSrc when props.imgSrc is truthy', () => {
    // Arrange
    const props = {
        imgSrc: 'image.jpg',
        width: 100,
        height: 100,
        setImgSrc: jest.fn()
    };

    // Act
    const wrapper = shallow(<WebCamFrame {...props} />);

    // Assert
    expect(wrapper.find('.WebCamFrameImg')).toHaveLength(1);
    expect(wrapper.find('.WebCamFrameImg').prop('src')).toEqual('image.jpg');
});

