import React from 'react';
import NavBar from "../components/NavBar";
import Network from "../classes/Network";
import CandleStick from "../components/CandleStick";
import CircularProgress from "@material-ui/core/CircularProgress";
import './Home.css';
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import TrendingUpIcon from '@material-ui/icons/TrendingUp';
import TrendingDownIcon from '@material-ui/icons/TrendingDown';

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
    try{
      this.setState({change:JSON.parse(prediction).percentChange});
    }catch (e) {
      console.log(prediction);
      console.log(e);
    }
  };

  gotData = (data)=>{
    try{
      this.setState({
        data:JSON.parse(data)
      });
    }catch (e) {
      console.log(data);
      console.log(e);
    }

  };
  onError = (err)=>{
    console.error(err);
  };

  updateName = (name)=>{
    this.setState(name);
  };

  render() {
    let change = null;
    if(this.state.change){
      let icon = this.state.change>0?<TrendingUpIcon fontSize='inherit'/>:<TrendingDownIcon fontSize='inherit'/>;
      change = <Typography variant='h3' className={'change '+((this.state.change>0)?'up':'down')}>Prediction: {this.state.change*100}% {icon}</Typography>
    }
    let data = null;
    if(this.state.data){
      data = (<Paper className='candleStick'>
        <div className='candleStickContainer'>
          <CandleStick data={this.state.data}/>
        </div>
      </Paper>);
    }
    let loading = (!change || !data)?<CircularProgress />:null;
    return (
      <div className='home'>
        <NavBar pageName='Home' updateName={this.updateName}/>
        <div className='name'>
          <Typography variant='h1'>{this.state.name}</Typography>
          {!loading && change}
        </div>
        {!loading && data}
        {loading}
      </div>
    );
  };
}

export default Home;