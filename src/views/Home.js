import React from 'react';
import NavBar from "../components/NavBar";
import Network from "../classes/Network";
import CandleStick from "../components/CandleStick";
import CircularProgress from "@material-ui/core/CircularProgress";

class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data:null,
      name:this.props.name?this.props.name:'ETH',
      change:null,
    }
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if(prevState.name !== this.state.name){
      Network.getData(this.state.name, this.gotData, this.onError);
      Network.predict(this.state.name, '2020-02-8', this.gotPrediction, this.onError);
    }
  }

  componentDidMount() {
    Network.getData(this.state.name, this.gotData, this.onError);
    Network.predict(this.state.name, '2020-02-8', this.gotPrediction, this.onError);
  }

  gotPrediction = (prediction)=>{
    this.setState({change:JSON.parse(prediction).percentChange});
  };

  gotData = (data)=>{
    this.setState({
      data:JSON.parse(data)
    });
  };
  onError = (err)=>{
    console.error(err);
  };

  render() {
    return (
      <div className='home'>
        <NavBar pageName='Home'/>
        <h1>{this.state.name}</h1>
        {this.state.data?<CandleStick className='candleStick' data={this.state.data}/>:<CircularProgress />}
        {this.state.change?<h2>{this.state.change}</h2>:<div/>}
      </div>
    );
  };
}

export default Home;