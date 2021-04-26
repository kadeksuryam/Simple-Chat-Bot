import React from 'react'
import axios from 'axios'
import { Chat } from '@progress/kendo-react-conversational-ui';
import '@progress/kendo-theme-material/dist/all.css';
import './app.css'
import { BrowserRouter as Router,
    Route,
    Switch } from "react-router-dom"
import Navbar from './components/Navbar';
import About from './components/About'

class App extends React.Component {
  constructor(props) {
      super(props);
      this.user = {
          id: 1,
          avatarUrl: "https://via.placeholder.com/24/008000/008000.png"
      };
      this.bot = { id: 0, avatarUrl: "https://ih0.redbubble.net/image.704526441.8813/flat,1000x1000,075,f.jpg" };
      this.state = {
          messages: [
              {
                  author: this.bot,
                  suggestedActions: [
                      {
                          type: 'reply',
                          value: 'What can you do?'
                      }
                  ],
                  timestamp: new Date(),
                  text: "Hello, my name is Hayacaka <3 I'm a Deadline Remainder Assistant, よろしくお願いします!"
              }
          ],
          time : 0
      };
  }

  componentDidMount() {
    this.fetchTime();
  }

  addNewMessage = async (event) => {
      let botResponse = Object.assign({}, event.message);
      let serverRes = await this.getResponse(event.message.text);
      botResponse.text = serverRes.res_msg
      botResponse.author = this.bot;
      this.setState((prevState) => ({
          messages: [
              ...prevState.messages,
              event.message
          ]
      }));
      setTimeout(() => {
          this.setState(prevState => ({
              messages: [
                  ...prevState.messages,
                  botResponse
              ]
          }));
      }, 1000);
  };

  getResponse = async (req_msg) => {
     // Respon berbentuk JSON : { "timestamp: ", "data" : {"res_message": "", "res_suggestion" : ["", ""]}}
     let res = await axios.post('/api', {"message" : req_msg})
     return {timestamp: res.data.timestamp, res_msg: res.data.res_msg, res_msg_sgt: res.data.res_msg_sgt}
  }

  countReplayLength = (question) => {
      let length = question.length;
      let answer = question + " contains exactly " + length + " symbols.";
      return answer;
  }

  fetchTime = async () => {
      const realTime = await axios.get('/api/time');
      this.setState({time : realTime.data.time});
    //   console.log(realTime);
  }

  render() {
      return (
        <div>
          <Router>
              <Navbar/>
              <Switch>
                  <Route path="/about">
                    <About />
                  </Route>
                  <Route path="/">
                    <Chat className="chat-container" user={this.user}
                messages={this.state.messages}
                onMessageSend={this.addNewMessage}
                placeholder={"Masukkan suatu perintah..."}/>
                  </Route>
              </Switch>
          </Router>
        </div>
      );
  }
}

export default App;
