import {shallow} from 'enzyme';
import App from "../../App";
import {configure} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({adapter: new Adapter()});


it('should use BrowserRouter and Routes components from react-router-dom to handle routing', () => {
    // Arrange
    const wrapper = shallow(<App/>);

    // Act
    const browserRouter = wrapper.find('BrowserRouter');
    const routes = wrapper.find('Routes');

    // Assert
    expect(browserRouter.exists()).toBe(true);
    expect(routes.exists()).toBe(true);
});

