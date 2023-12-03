// import {configure} from 'enzyme';
// import Adapter from 'enzyme-adapter-react-16';
// import {shallow} from 'enzyme';
// import MusicParameters from "../MusicParameters";
// import {render, screen} from '@testing-library/react';
// import * as fireEvent from "react-dom/test-utils";

// configure({adapter: new Adapter()});

// describe('MusicParameters', () => {
//   test('renders MusicParameters component', () => {
//     const initialMusicParameter1 = 'high';
//     const initialMusicParameter2 = 'medium';

//     render(
//       <MusicParameters
//         musicParameter1="initialMusicParameter1"
//         musicParameter2="initialMusicParameter2"
//         setMusicParameter1={() => {}}
//         setMusicParameter2={() => {}}
//       />
//     );
//     const select1 = screen.getByText('Popularity');
//     const select2 = screen.getByText('Personalization');

//     expect(select1).toHaveValue(initialMusicParameter1);
//     expect(select2).toHaveValue(initialMusicParameter2);
//   });
// });