import ImageUploadFrame from '../ImageUploadFrame'
import {shallow} from 'enzyme';
import App from "../../App";
import {configure} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({adapter: new Adapter()});
it('should render an input element with class \'imageUploadFrameBox\' when props.imgSrc is null', () => {
    const props = {
        imgSrc: null,
        setImgSrc: jest.fn(),
        width: 100,
        height: 100
    };

    const wrapper = shallow(<ImageUploadFrame {...props} />);
    expect(wrapper.find('input').hasClass('imageUploadFrameBox')).toBe(true);
});
it('should render an image element with src equal to props.imgSrc when props.imgSrc is not null', () => {
    const props = {
        imgSrc: 'image.jpg',
        setImgSrc: jest.fn(),
        width: 100,
        height: 100
    };

    const wrapper = shallow(<ImageUploadFrame {...props} />);
    expect(wrapper.find('img').prop('src')).toBe(props.imgSrc);
});
it('should set the maximum width and height of the image element to props.width and props.height respectively', () => {
    const props = {
        imgSrc: 'image.jpg',
        setImgSrc: jest.fn(),
        width: 100,
        height: 200
    };

    const wrapper = shallow(<ImageUploadFrame {...props} />);
    expect(wrapper.find('img').prop('style')).toEqual({maxWidth: props.width, maxHeight: props.height});
});
it('should render an input element with type \'file\' and accept attribute set to \'image/*\'', () => {
    const props = {
        imgSrc: null,
        setImgSrc: jest.fn(),
        width: 100,
        height: 100
    };

    const wrapper = shallow(<ImageUploadFrame {...props} />);
    expect(wrapper.find('input').prop('type')).toBe('file');
    expect(wrapper.find('input').prop('accept')).toBe('image/*');
});
it('should not call props.setImgSrc when no file is selected', () => {
    const props = {
        imgSrc: null,
        setImgSrc: jest.fn(),
        width: 100,
        height: 100
    };

    const wrapper = shallow(<ImageUploadFrame {...props} />);
    wrapper.find('input').simulate('change', {target: {files: []}});
    expect(props.setImgSrc).not.toHaveBeenCalled();
});
it('should not render an image element when props.imgSrc is null', () => {
    const props = {
        imgSrc: null,
        setImgSrc: jest.fn(),
        width: 100,
        height: 100
    };

    const wrapper = shallow(<ImageUploadFrame {...props} />);
    expect(wrapper.find('img').exists()).toBe(false);
});