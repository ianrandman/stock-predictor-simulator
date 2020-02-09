import React from 'react';
import NavBar from "../components/NavBar";
import Network from "../classes/Network";
import CandleStick from "../components/CandleStick";
import CircularProgress from "@material-ui/core/CircularProgress";
import './Home.css';
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
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
    console.log(JSON.parse(prediction));
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
    let change = null;
    if(this.state.change){
      let icon = this.state.change>0?<TrendingUpIcon/>:<TrendingDownIcon/>;
      change = <Typography variant='h1' className={'change '+((this.state.change>0)?'up':'down')}>Prediction: {this.state.change}% {icon}</Typography>
    }
    return (
      <div className='home'>
        <NavBar pageName='Home'/>
        <Typography variant='h1'>{this.state.name}{change}</Typography>
        <Paper className='candleStick'>
          <div className='candleStickContainer'>
            {this.state.data?<CandleStick data={this.state.data}/>:<CircularProgress />}
          </div>
        </Paper>
      </div>
    );
  };
}

export default Home;