// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Vote {
  struct Voter {    // Information about voter
    bool voted;
    uint voteIdx;
  }
  struct Proposal {    // A struct for each proposal
    bytes32 name;
    uint voteCount;
  }

  mapping(address => Voter) private voter;    // state variable that store 'Voter' struct for each possible address
  Proposal[4] public proposals;
  uint deadline;    // Time to finish voting

  constructor() {    // Just give data statically
    proposals[0] = Proposal({name: unicode"기호 1번", voteCount: 0});
    proposals[1] = Proposal({name: unicode"기호 2번", voteCount: 0});
    proposals[2] = Proposal({name: unicode"기호 3번", voteCount: 0});
    proposals[3] = Proposal({name: unicode"기호 4번", voteCount: 0});
    deadline = block.timestamp + 1 minutes;    // Setting voting time 1 minute to easy debugging. block.timestamp gives block created time.
    voter[msg.sender] = Voter({voted: false, voteIdx: 5});    // Register chairman to voter, voteIdx = 5 means doesn't vote yet.
  }

  modifier noDuplicateVote {    // If msg.sender already voted, he can't!
    require(!voter[msg.sender].voted, "Already Voted");
    _;
  }

  function vote(uint _idx, uint _voteTime) external noDuplicateVote {
    require(_voteTime < deadline, "Time Over");
    Voter storage sender = voter[msg.sender];
    sender.voted = true;
    sender.voteIdx = _idx - 1;    // Because voter will give 1 ~ 4.
    proposals[_idx - 1].voteCount += 1;
  }

  function checkWinner() private view returns (uint) {
    uint maxVoteCount = 0;
    uint winnerIdx = 0;
    for (uint i=1; i<proposals.length; i++) {
      if (proposals[i].voteCount > maxVoteCount) {
        maxVoteCount = proposals[i].voteCount;
        winnerIdx = i;
      }
    }
    return winnerIdx;
  }

  function giveWinnerName(uint _requestTime) public view returns (bytes32) {
    require(_requestTime >= deadline, "Wait for end");
    bytes32 winnerName = proposals[checkWinner()].name;
    return winnerName;
  }
}
