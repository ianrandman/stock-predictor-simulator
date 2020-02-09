export default class Network{
  static  getData = (stock, successCallback, failCallback)=>{
    window.fetch(`http://f4e46a3c-11e7-47e4-92ab-fd169ac7e057.mock.pstmn.io/data?stock=${stock}`, {mode: 'no-cors',}).then((resp)=>{
      if(resp.ok){
        resp.text().then((json)=>{
          successCallback(json);
        });
      }else{
        resp.text().then((json)=>{
          failCallback(json);
        });
      }
    })
  };

  static predict = (stock, date, successCallback, failCallback)=>{
    window.fetch(`https://api-dot-stock-predictor-simulator.appspot.com/predict?stock=${stock}&date=${date}`, {mode: 'no-cors',}).then((resp)=>{
      if(resp.ok){
        resp.text().then((json)=>{
          console.log(json);
          successCallback(json);
        });
      }else{
        resp.text().then((json)=>{
          failCallback(json);
        });
      }
    })
  }
  static getOptions = ()=>{
    return window.fetch(`https://api-dot-stock-predictor-simulator.appspot.com/list`, {mode: 'no-cors',})
  }
}