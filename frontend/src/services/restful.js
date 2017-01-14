import Restful from 'restful-fetch';

const restful = new Restful({
  root: '/api',
});

export default restful;

export const My = restful.model('my');
My.Polls = My.model('polls');

export const Polls = restful.model('polls');
