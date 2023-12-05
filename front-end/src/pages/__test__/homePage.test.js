import {shallow} from 'enzyme';
import HomePage from "../HomePage";
import {configure, mount} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({adapter: new Adapter()});

    it('should render the home page frame with a description and a music recommendation button', () => {
      const wrapper = shallow(<HomePage />);
      expect(wrapper.find('.homePageFrame')).toHaveLength(1);
      expect(wrapper.find('.homePageDescription')).toHaveLength(1);
      expect(wrapper.find('.homePageButton')).toHaveLength(1);
    });

