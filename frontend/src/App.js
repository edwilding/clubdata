import React from "react";
import './App.css';
import AsyncSelect from 'react-select/async';
import 'bootstrap/dist/css/bootstrap.min.css';


function isInt(value) {
  return !isNaN(value) && 
         parseInt(Number(value)) == value && 
         !isNaN(parseInt(value, 10));
}


const TeamLookup = () => {

  const [opt1, setOpt1] = React.useState([])
  const [opt2, setOpt2] = React.useState([])
  const [data, setData] = React.useState([])

  const loadOptions = (inputValue, callback) => {
    const url = `http://51.254.202.9:11111/clubs/?search=${inputValue}`;
  
    fetch(url)
    .then(resp => resp.json())
    .then(resp => {
      const toSelectOption = ({ id, name }) => ({ label: name, value: id });
      // map server data to options
      const asyncOptions = resp.map(toSelectOption);
      // Call callback with mapped options
      callback(asyncOptions);
    })
  };

  React.useEffect(() => {
    if (isInt(opt1) && isInt(opt2)) {
      fetch(`http://51.254.202.9:11111/matches/?team1=${opt1}&team2=${opt2}`)
      .then(resp => resp.json())
      .then((data) => setData(data))
    }
  }, [opt1, opt2]);

  function TeamData(props) {
    if (data && data.count > 0) {
      const win_percent = ((data.wins / data.count) * 100).toFixed(2)
      const draw_percent = ((data.draws / data.count) * 100).toFixed(2)
      const loss_percent = ((data.losses / data.count) * 100).toFixed(2)
      return (
        <div className="progress my-4">
          <div className="progress-bar bg-success" role="progressbar" style={{width: win_percent + "%"}} aria-valuenow="15" aria-valuemin="0" aria-valuemax="100">{data.wins}</div>
          <div className="progress-bar bg-secondary" role="progressbar" style={{width: draw_percent + "%"}} aria-valuenow="30" aria-valuemin="0" aria-valuemax="100">{data.draws}</div>
          <div className="progress-bar bg-danger" role="progressbar" style={{width: loss_percent + "%"}} aria-valuenow="20" aria-valuemin="0" aria-valuemax="100">{data.losses}</div>
        </div>
      )
      //return <div>wins: {data.wins}, draws: {data.draws}, losses: {data.losses}</div>
    } else if (data) {
      return <div className="text-light mt-4">No Games Found</div>
    }
    return <div></div>
  }

  function MatchData(props) {
    if (data && data.count > 0) {
      return (
        <div className="row mt-4">
          <h4 className="text-white">Recent Games</h4>
          <div className="card bg-dark text-white">
            <ul className="list-group list-group-flush">
              {data.results.map((i) => <li className="list-group-item bg-dark text-white"><small>{i.date} | {i.home.name} {i.home_goals} - {i.away_goals} {i.away.name}</small></li>)}
            </ul>
          </div>
        </div>
      ) 
    }
    return <div></div>
  }

  return ( 
    <div>

      <div class="content p-4 mb-3 shadow rounded text-center bg-dark">
        <div class="row justify-content-center">
          <h1 class="text-light" >Footie H2H Stats</h1>
        </div>
      </div>

      <div className="content p-4 shadow rounded text-center bg-dark">
        <div className="row justify-content-center">
          <div className="col-lg-5">
            <AsyncSelect
              className="my-1"
              noOptionsMessage={() => 'No Clubs Found :('}
              loadOptions={loadOptions}
              onChange={opt => setOpt1(opt.value)}
            />
          </div>
          <div className="col-lg-2 justify-content-center"><h1><span className="font-weight-bold text-light">Vs.</span></h1></div>
          <div className="col-lg-5">
            <AsyncSelect
              className="my-1"
              noOptionsMessage={() => 'No Clubs Found :('}
              loadOptions={loadOptions}
              onChange={opt => setOpt2(opt.value)}
            />
          </div>
        </div>
        <TeamData />
        <MatchData />
      </div>
    </div>
    
  );
};


function App() {
  return (
    <div>
      <TeamLookup />
    </div>
  );
}

export default App;
